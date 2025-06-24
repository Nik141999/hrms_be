from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
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
    new_leave = await create_leave_in_db(db, leave, user_id)
    return LeaveResponse.model_validate(new_leave)

async def get_all_leaves_service(db: AsyncSession, page: int, limit: int) -> PaginatedLeaveResponse:
    skip = (page - 1) * limit
    total = await get_total_leave_count(db)
    leaves = await get_all_leaves_by_user_id(db, skip=skip, limit=limit)

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
