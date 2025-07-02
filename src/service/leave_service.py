from sqlalchemy import func
from sqlalchemy.future import select
from fastapi import HTTPException, status
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from src.enums.leave_enums import LeaveStatus

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

    user_result = await db.execute(select(User).where(User.id == user_id))
    current_user = user_result.scalar_one_or_none()

    if not current_user or not current_user.department_id:
        raise HTTPException(status_code=400, detail="User or user's department not found")

    department_id = current_user.department_id
    role_type = current_user.role.role_type.lower()

    reviewer_id = None
    manager_id = None

    # If employee, assign to least busy HR and department manager
    if role_type == "employee":
        # Get HRs in the department
        hr_result = await db.execute(
            select(User)
            .join(Role)
            .where(Role.role_type == "hr", User.department_id == department_id)
        )
        hr_users = hr_result.scalars().all()

        if not hr_users:
            raise HTTPException(status_code=404, detail="No HR found in your department")

        # Pick HR with fewest leaves
        hr_with_counts = []
        for hr in hr_users:
            count_result = await db.execute(
                select(func.count()).select_from(Leave).where(Leave.reviewer_id == hr.id)
            )
            count = count_result.scalar_one()
            hr_with_counts.append((hr, count))

        least_busy_hr = min(hr_with_counts, key=lambda x: x[1])[0]
        reviewer_id = least_busy_hr.id

    # HR creating a leave (or employee)—assign manager
    if role_type in ["employee", "hr"]:
        mgr_result = await db.execute(
            select(User)
            .join(Role)
            .where(Role.role_type == "manager", User.department_id == department_id)
        )
        manager = mgr_result.scalars().first()
        if not manager:
            raise HTTPException(status_code=404, detail="No Manager found in your department")
        manager_id = manager.id

    # Optional: handle Admin creating leave (if needed)
    if role_type == "admin":
        raise HTTPException(status_code=403, detail="Admins cannot apply for leaves.")

    # Create leave with selected reviewer_id (can be None) and manager_id
    new_leave = await create_leave_in_db(
        db, leave, user_id, reviewer_id=reviewer_id, manager_id=manager_id
    )
    return LeaveResponse.model_validate(new_leave)

async def get_all_leaves_service(db: AsyncSession, page: int, limit: int, current_user: User) -> PaginatedLeaveResponse:
    skip = (page - 1) * limit
    role_type = current_user.role.role_type.lower()

    if role_type == "hr":
        # HR sees only the leaves they are assigned to review
        query = select(Leave).where(Leave.reviewer_id == current_user.id)
        count_query = select(func.count()).select_from(Leave).where(Leave.reviewer_id == current_user.id)

    elif role_type == "manager":
        # Manager sees only the leaves assigned to them as manager
        query = select(Leave).where(Leave.manager_id == current_user.id)
        count_query = select(func.count()).select_from(Leave).where(Leave.manager_id == current_user.id)
        
    elif role_type == "admin":
        # Admin sees all leaves
        query = select(Leave)
        count_query = select(func.count()).select_from(Leave)    

    else:
       query = select(Leave).where(Leave.user_id == current_user.id)
       count_query = select(func.count()).select_from(Leave).where(Leave.user_id == current_user.id)


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

async def update_leave_status_service(leave_id: str, status: str, db: AsyncSession, current_user: User):
    if current_user.role.role_type.lower() != "hr":
        raise HTTPException(status_code=403, detail="Only HR can update leave status.")

    result = await db.execute(select(Leave).where(Leave.id == leave_id))
    leave = result.scalar_one_or_none()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if leave.reviewer_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not assigned to review this leave.")

    if leave.status != LeaveStatus.PENDING:
        raise HTTPException(status_code=400, detail="Only pending leaves can be updated.")

    try:
        new_status = LeaveStatus(status.upper())  # 🧠 fix is here
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status. Use: ACCEPTED, REJECTED")

    leave.status = new_status
    await db.commit()
    await db.refresh(leave)

    return LeaveResponse.model_validate(leave)