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
    get_leave_by_id_and_user,
    update_leave_in_db,
    delete_leave_in_db,
    get_total_leave_count
)
from src.schemas.leave_schema import LeaveCreate, LeaveResponse, LeaveUpdate, PaginatedLeaveResponse

async def create_leave_service(leave: LeaveCreate, db: AsyncSession, user_id: str) -> LeaveResponse:
    if leave.start_date < date.today():
        raise ValueError("Start date cannot be in the past.")

    # Fetch current user
    user_result = await db.execute(select(User).where(User.id == user_id))
    current_user = user_result.scalar_one_or_none()

    if not current_user or not current_user.department_id or not current_user.organization_id:
        raise HTTPException(status_code=400, detail="User, department, or organization not found")

    department_id = current_user.department_id
    organization_id = current_user.organization_id
    role_type = current_user.role.role_type.lower()

    # Admins cannot apply for leave
    if role_type == "admin":
        raise HTTPException(status_code=403, detail="Admins cannot apply for leaves.")

    reviewer_id = None
    manager_id = None

    # If employee, assign HR reviewer
    if role_type == "employee":
        hr_result = await db.execute(
            select(User)
            .join(Role)
            .where(
                Role.role_type == "hr",
                User.department_id == department_id,
                User.organization_id == organization_id
            )
        )
        hr_user = hr_result.scalars().first()

        if not hr_user:
            raise HTTPException(status_code=404, detail="No HR found in your department and organization")

        reviewer_id = hr_user.id

    # Always assign manager if employee or HR
    if role_type in ["employee", "hr"]:
        mgr_result = await db.execute(
            select(User)
            .join(Role)
            .where(
                Role.role_type == "manager",
                User.department_id == department_id,
                User.organization_id == organization_id
            )
        )
        manager = mgr_result.scalars().first()

        if not manager:
            raise HTTPException(status_code=404, detail="No Manager found in your department and organization")

        manager_id = manager.id

    # Create leave request
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

async def update_leave_status_service(leave_id: str, status: str, db, current_user: User):
    role = current_user.role.role_type.lower()

    result = await db.execute(select(Leave).where(Leave.id == leave_id))
    leave = result.scalar_one_or_none()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if role not in ["hr", "manager"]:
        raise HTTPException(status_code=403, detail="Only HR or Manager can update leave status")

    if role == "hr":
        if leave.reviewer_id != current_user.id:
            raise HTTPException(status_code=403, detail="You are not assigned to review this leave.")
    if role == "manager":
        if leave.manager_id != current_user.id:
            raise HTTPException(status_code=403, detail="You are not assigned as manager for this leave.")

    try:
        new_status = LeaveStatus(status.upper())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status")

    if role == "hr":
        leave.hr_status = new_status
    elif role == "manager":
        leave.manager_status = new_status

    # Determine final status
    if leave.hr_status == LeaveStatus.REJECTED or leave.manager_status == LeaveStatus.REJECTED:
        leave.status = LeaveStatus.REJECTED
    elif leave.reviewer_id and leave.hr_status == LeaveStatus.ACCEPTED and leave.manager_status == LeaveStatus.ACCEPTED:
        leave.status = LeaveStatus.ACCEPTED
    elif not leave.reviewer_id and leave.manager_status == LeaveStatus.ACCEPTED:
        leave.status = LeaveStatus.ACCEPTED
    else:
        leave.status = LeaveStatus.PENDING

    await db.commit()
    await db.refresh(leave)
    return LeaveResponse.model_validate(leave)
