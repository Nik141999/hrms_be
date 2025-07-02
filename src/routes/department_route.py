from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.auth import get_current_user
from src.utils.permission_checker import PermissionChecker
from src.controller.department_controller import *
from src.schemas.department_schema import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
    PaginatedDepartmentResponse
)
from src.database import get_db

router = APIRouter(tags=["Department"], dependencies=[Depends(get_current_user)])

@router.post("/department", response_model=DepartmentResponse,
             dependencies=[Depends(PermissionChecker("/department", "create"))])
async def create_department(
    dept: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await create_dept_controller(dept, db, current_user)


@router.get("/department", response_model=PaginatedDepartmentResponse,
            dependencies=[Depends(PermissionChecker("/department", "view"))])
async def get_departments(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db),
    search: str = Query(None),
    current_user=Depends(get_current_user)  # Logged-in Organization
):
    return await get_all_dept_controller(db, page, limit, search, current_user)


@router.put("/department/{dept_id}", response_model=DepartmentResponse,
            dependencies=[Depends(PermissionChecker("/department/{dept_id}", "edit"))])
async def update_department(dept_id: str, dept_data: DepartmentUpdate, db: AsyncSession = Depends(get_db)):
    return await update_dept_controller(dept_id, dept_data, db)

@router.delete("/department/{dept_id}",
               dependencies=[Depends(PermissionChecker("/department/{dept_id}", "delete"))])
async def delete_department(dept_id: str, db: AsyncSession = Depends(get_db)):
    return await delete_dept_controller(dept_id, db)
