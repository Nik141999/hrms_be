from src.models.department import Department
from uuid import uuid4
from sqlalchemy.future import select

async def create_department_dao(dept_data, db):
    new_dept = Department(id=str(uuid4()), department_name=dept_data.department_name)
    db.add(new_dept)
    await db.commit()
    await db.refresh(new_dept)
    return new_dept

async def get_all_departments_dao(db):
    result = await db.execute(select(Department))
    return result.scalars().all()

async def update_department_dao(dept_id, dept_data, db):
    result = await db.execute(select(Department).where(Department.id == dept_id))
    dept = result.scalars().first()
    if not dept:
        raise Exception("Department not found")

    if dept_data.department_name is not None:
        dept.department_name = dept_data.department_name

    await db.commit()
    await db.refresh(dept)
    return dept

async def delete_department_dao(dept_id, db):
    result = await db.execute(select(Department).where(Department.id == dept_id))
    dept = result.scalars().first()
    if not dept:
        raise Exception("Department not found")

    await db.delete(dept)
    await db.commit()
    return {"detail": "Department deleted successfully"}
