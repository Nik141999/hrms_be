from sqlalchemy import func
from sqlalchemy.future import select
from fastapi import HTTPException, status
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.models.role import Role
from src.models.leave import Leave
from src.dao.leave_dao import (
    create_leave_in_db,
    get_all_leaves_by_user_id,
    get_leave_by_id_and_user,
    update_leave_in_db,
    delete_leave_in_db,
    get_total_leave_count
)
from src.schemas.leave_schema import LeaveCreate, LeaveResponse, LeaveUpdate, PaginatedLeaveResponse

async def create_leave_service(leave: LeaveCreate, db: AsyncSession, user_id: str) -> LeaveResponse:
    if leave.start_date < date.today():
        raise ValueError("Start date cannot be in the past.")

    # Step 1: Get the current user to find their department
    user_result = await db.execute(select(User).where(User.id == user_id))
    current_user = user_result.scalar_one_or_none()

    if not current_user or not current_user.department_id:
        raise HTTPException(status_code=400, detail="User or user's department not found")

    department_id = current_user.department_id

    # Step 2: Get HRs in the same department
    hr_result = await db.execute(
        select(User)
        .join(Role)
        .where(
            Role.role_type == "hr",
            User.department_id == department_id
        )
    )
    hr_users = hr_result.scalars().all()

    if not hr_users:
        raise HTTPException(status_code=404, detail="No HR found in your department")

    # Step 3: Find the HR with the fewest assigned leaves
    hr_with_counts = []
    for hr in hr_users:
        count_result = await db.execute(
            select(func.count()).select_from(Leave).where(Leave.reviewer_id == hr.id)
        )
        count = count_result.scalar_one()
        hr_with_counts.append((hr, count))

    least_busy_hr = min(hr_with_counts, key=lambda x: x[1])[0]

    # Step 4: Create the leave and assign the HR as reviewer
    new_leave = await create_leave_in_db(db, leave, user_id, reviewer_id=least_busy_hr.id)

    return LeaveResponse.model_validate(new_leave)

async def get_all_leaves_service(db: AsyncSession, page: int, limit: int, current_user: User) -> PaginatedLeaveResponse:
    skip = (page - 1) * limit

    role_type = current_user.role.role_type.lower()

    if role_type == "hr":
        query = select(Leave).where(Leave.reviewer_id == current_user.id)
        count_query = select(func.count()).select_from(Leave).where(Leave.reviewer_id == current_user.id)
    else:
        query = select(Leave)
        count_query = select(func.count()).select_from(Leave)

    leaves_result = await db.execute(query.offset(skip).limit(limit))
    count_result = await db.execute(count_query)

    leaves = leaves_result.scalars().all()
    total = count_result.scalar_one()

    return PaginatedLeaveResponse(
        totalItems=total,
        totalPages=(total + limit - 1) // limit,
        currentPage=page,
        pageSize=limit,
        leaves=[LeaveResponse.model_validate(leave) for leave in leaves]
    )


async def update_leave_service(leave_id: int, leave: LeaveUpdate, db: AsyncSession, user_id: str):
    existing_leave = await get_leave_by_id_and_user(db, leave_id, user_id)
    if not existing_leave:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave not found")
    updated_leave = await update_leave_in_db(db, existing_leave, leave)
    return LeaveResponse.model_validate(updated_leave)

async def delete_leave_service(leave_id: int, db: AsyncSession, user_id: str):
    existing_leave = await get_leave_by_id_and_user(db, leave_id, user_id)
    if not existing_leave:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave not found")
    await delete_leave_in_db(db, existing_leave)
    return {"message": "Leave deleted successfully"}
