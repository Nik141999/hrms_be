from src.models.department import Department
from uuid import uuid4
from sqlalchemy.future import select
from sqlalchemy import func

async def create_department_dao(dept_data, db, current_user):
    new_dept = Department(
        id=str(uuid4()),
        department_name=dept_data.department_name,
        organization_id=current_user.id

    )
    db.add(new_dept)
    await db.commit()
    await db.refresh(new_dept)
    return new_dept

async def get_paginated_departments_dao(db, skip: int, limit: int, search: str = None, organization_id: str = None):
    stmt = select(Department)

    if search:
        stmt = stmt.where(Department.department_name.ilike(f"%{search}%"))

    if organization_id:
        stmt = stmt.where(Department.organization_id == organization_id)

    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_total_departments_count(db, search: str = None, organization_id: str = None):
    stmt = select(func.count()).select_from(Department)

    if search:
        stmt = stmt.where(Department.department_name.ilike(f"%{search}%"))

    if organization_id:
        stmt = stmt.where(Department.organization_id == organization_id)

    result = await db.execute(stmt)
    return result.scalar_one()


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
