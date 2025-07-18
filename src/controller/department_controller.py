from src.service.department_service import *

async def create_dept_controller(dept_data, db, current_user):
    return await create_department_service(dept_data, db, current_user)

async def get_all_dept_controller(db, page: int, limit: int, search: str, current_user):
    return await get_all_departments_service(db, page, limit, search, current_user)

async def update_dept_controller(dept_id, dept_data, db):
    return await update_department_service(dept_id, dept_data, db)

async def delete_dept_controller(dept_id, db):
    return await delete_department_service(dept_id, db)
