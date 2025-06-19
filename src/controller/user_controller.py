from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user import UserCreate, UserUpdate, UserResponse
from src.service.user_service import (
    create_user_service,
    get_user_service,
    update_user_service,
    delete_user_service,
    get_all_users_service
)

async def create_user_controller(user: UserCreate, db: AsyncSession, org_id: str):
    try:
        return await create_user_service(user, db, org_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

async def get_user_controller(user_id: str, db: AsyncSession):
    try:
        return await get_user_service(user_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

async def get_all_users_controller(db: AsyncSession):
    return await get_all_users_service(db)

async def update_user_controller(user_id: str, user_update: UserUpdate, db: AsyncSession):
    try:
        return await update_user_service(user_id, user_update, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

async def delete_user_controller(user_id: str, db: AsyncSession):
    try:
        return await delete_user_service(user_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
