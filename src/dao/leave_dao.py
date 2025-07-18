from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from src.models.leave import Leave
from src.schemas.leave_schema import LeaveCreate, LeaveUpdate
from src.enums.leave_enums import LeaveStatus

async def create_leave_in_db(db: AsyncSession, leave: LeaveCreate, user_id: str, reviewer_id: str, manager_id: str):
    new_leave = Leave(
        user_id=user_id,
        reviewer_id=reviewer_id,
        manager_id=manager_id,
        leave_type=leave.leave_type,
        description=leave.description,
        start_date=leave.start_date,
        end_date=leave.end_date,
        hr_status=LeaveStatus.PENDING if reviewer_id else None,
        manager_status=LeaveStatus.PENDING,
        status=LeaveStatus.PENDING
    )
    db.add(new_leave)
    await db.commit()
    await db.refresh(new_leave)
    return new_leave

async def get_total_leave_count(db: AsyncSession) -> int:
    result = await db.execute(select(func.count()).select_from(Leave))
    return result.scalar_one()

async def get_leave_by_id_and_user(db: AsyncSession, leave_id: int, user_id: str):
    result = await db.execute(
        select(Leave).where(Leave.id == leave_id, Leave.user_id == user_id)
    )
    return result.scalar_one_or_none()

async def update_leave_in_db(db: AsyncSession, leave_obj: Leave, leave_update: LeaveUpdate):
    if leave_update.leave_type is not None:
        leave_obj.leave_type = leave_update.leave_type
    if leave_update.description is not None:
        leave_obj.description = leave_update.description
    if leave_update.start_date is not None:
        leave_obj.start_date = leave_update.start_date
    if leave_update.end_date is not None:
        leave_obj.end_date = leave_update.end_date

    await db.commit()
    await db.refresh(leave_obj)
    return leave_obj

async def delete_leave_in_db(db: AsyncSession, leave_obj: Leave):
    await db.delete(leave_obj)
    await db.commit()