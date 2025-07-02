from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.auth import get_current_user
from src.schemas.leave_schema import LeaveCreate, LeaveResponse, LeaveUpdate, PaginatedLeaveResponse
from src.utils.permission_checker import PermissionChecker
from src.controller.leave_controller import (
    create_leave_controller,
    get_all_leaves_controller,
    update_leave_controller,
    delete_leave_controller,
    update_leave_status_controller
)
from src.database import get_db
from src.models.user import User

router = APIRouter(tags=["Leave"])


@router.post("/leaves", response_model=LeaveResponse)
async def create_leave(
    leave: LeaveCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_leave_controller(leave, db, current_user.id)

@router.get("/leaves", response_model=PaginatedLeaveResponse, dependencies=[Depends(PermissionChecker("/leaves", "view"))])
async def get_all_leaves(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_all_leaves_controller(db, page, limit, current_user)

@router.put("/leaves/{leave_id}", response_model=LeaveResponse, dependencies=[Depends(PermissionChecker("/leaves/{leave_id}", "edit"))])
async def update_leave(
    leave_id: str,
    leave: LeaveUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_leave_controller(leave_id, leave, db, current_user.id)

@router.delete("/leaves/{leave_id}", dependencies=[Depends(PermissionChecker("/leaves/{leave_id}", "delete"))])
async def delete_leave(
    leave_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await delete_leave_controller(leave_id, db, current_user.id)

@router.patch("/leaves/{leave_id}/status", response_model=LeaveResponse)
async def update_leave_status(
    leave_id: str,
    status: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_leave_status_controller(leave_id, status, db, current_user)
