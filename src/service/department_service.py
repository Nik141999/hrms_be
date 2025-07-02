from src.dao.department_dao import *
from src.schemas.department_schema import DepartmentResponse, PaginatedDepartmentResponse

async def create_department_service(dept_data, db, current_user):
    return await create_department_dao(dept_data, db, current_user)


async def get_all_departments_service(db, page: int, limit: int, search: str, current_user):
    skip = (page - 1) * limit

    # Handle both User and Organization login
    if hasattr(current_user, "organization_id"):
        organization_id = current_user.organization_id  # User login
    else:
        organization_id = current_user.id  # Organization login

    total = await get_total_departments_count(db, search=search, organization_id=organization_id)
    departments = await get_paginated_departments_dao(
        db, skip=skip, limit=limit, search=search, organization_id=organization_id
    )

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
