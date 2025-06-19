from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.auth import get_current_user
from src.controller.department_controller import *
from src.schemas.department_schema import DepartmentCreate, DepartmentResponse, DepartmentUpdate
from src.database import get_db

router = APIRouter(tags=["Department"], dependencies=[Depends(get_current_user)])

@router.post("/department", response_model=DepartmentResponse)
async def create_department(dept: DepartmentCreate, db: AsyncSession = Depends(get_db)):
    return await create_dept_controller(dept, db)

@router.get("/department", response_model=list[DepartmentResponse])
async def get_departments(db: AsyncSession = Depends(get_db)):
    return await get_all_dept_controller(db)

@router.put("/department/{dept_id}", response_model=DepartmentResponse)
async def update_department(dept_id: str, dept_data: DepartmentUpdate, db: AsyncSession = Depends(get_db)):
    return await update_dept_controller(dept_id, dept_data, db)

@router.delete("/department/{dept_id}")
async def delete_department(dept_id: str, db: AsyncSession = Depends(get_db)):
    return await delete_dept_controller(dept_id, db)
