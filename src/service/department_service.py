from src.dao.department_dao import *

async def create_department_service(dept_data, db):
    return await create_department_dao(dept_data, db)

async def get_all_departments_service(db):
    return await get_all_departments_dao(db)

async def update_department_service(dept_id, dept_data, db):
    return await update_department_dao(dept_id, dept_data, db)

async def delete_department_service(dept_id, db):
    return await delete_department_dao(dept_id, db)
