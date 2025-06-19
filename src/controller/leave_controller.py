from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.leave_schema import LeaveCreate, LeaveResponse, LeaveUpdate
from src.service.leave_service import (
    create_leave_service,
    get_all_leaves_service,
    update_leave_service,
    delete_leave_service,
)

async def create_leave_controller(leave: LeaveCreate, db: AsyncSession, user_id: str):
    try:
        return await create_leave_service(leave, db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

async def get_all_leaves_controller(db: AsyncSession):
    return await get_all_leaves_service(db)

async def update_leave_controller(leave_id: int, leave: LeaveUpdate, db: AsyncSession, user_id: str):
    return await update_leave_service(leave_id, leave, db, user_id)

async def delete_leave_controller(leave_id: int, db: AsyncSession, user_id: str):
    return await delete_leave_service(leave_id, db, user_id)
