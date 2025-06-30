from src.dao.department_dao import *
from src.schemas.department_schema import DepartmentResponse, PaginatedDepartmentResponse

async def create_department_service(dept_data, db):
    return await create_department_dao(dept_data, db)

async def get_all_departments_service(db, page: int, limit: int, search: str = None):
    skip = (page - 1) * limit
    total = await get_total_departments_count(db)
    departments = await get_paginated_departments_dao(db, skip=skip, limit=limit,search=search)

    return PaginatedDepartmentResponse(
        totalItems=total,
        totalPages=(total + limit - 1) // limit,
        currentPage=page,
        pageSize=limit,
        departments=[DepartmentResponse.model_validate(dept) for dept in departments]
    )

async def update_department_service(dept_id, dept_data, db):
    return await update_department_dao(dept_id, dept_data, db)

async def delete_department_service(dept_id, db):
    return await delete_department_dao(dept_id, db)
