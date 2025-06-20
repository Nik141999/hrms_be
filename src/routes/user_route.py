from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.auth import get_current_user
from src.utils.permission_checker import PermissionChecker
from src.controller.user_controller import (
    create_user_controller,
    get_user_controller,
    update_user_controller,
    delete_user_controller,
    get_all_users_controller
)
from src.schemas.user import UserCreate, UserResponse, UserUpdate
from src.database import get_db

router = APIRouter(tags=["User"], dependencies=[Depends(get_current_user)])

@router.post("/users", response_model=UserResponse, dependencies=[Depends(PermissionChecker("/users", "create"))])
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Determine organization_id based on whether the current user is an Organization or a User
    if hasattr(current_user, "org_name"):
        # Logged in as Organization
        org_id = current_user.id
    elif hasattr(current_user, "organization_id"):
        # Logged in as User
        org_id = current_user.organization_id
    else:
        raise HTTPException(status_code=400, detail="Could not determine organization context")

    return await create_user_controller(user, db, org_id)


@router.get("/users/{user_id}", response_model=UserResponse, dependencies=[Depends(PermissionChecker("/users/{user_id}", "view"))])
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    return await get_user_controller(user_id, db)


@router.get("/users", response_model=list[UserResponse], dependencies=[Depends(PermissionChecker("/users", "view"))])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await get_all_users_controller(db)


@router.put("/users/{user_id}", response_model=UserResponse, dependencies=[Depends(PermissionChecker("/users/{user_id}", "edit"))])
async def update_user(user_id: str, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    return await update_user_controller(user_id, user_update, db)


@router.delete("/users/{user_id}", dependencies=[Depends(PermissionChecker("/users/{user_id}", "delete"))])
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
    return await delete_user_controller(user_id, db)
