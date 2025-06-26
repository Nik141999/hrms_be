from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from sqlalchemy.orm import selectinload
from src.models.role import Role
from src.models.department import Department
from src.schemas.user import UserUpdate

async def get_role_by_name(db: AsyncSession, role_type: str):
    result = await db.execute(select(Role).where(Role.role_type == role_type.lower()))
    return result.scalars().first()

async def get_department_by_name(db: AsyncSession, department_name: str):
    result = await db.execute(select(Department).filter(Department.department_name == department_name))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def get_user_by_id(db: AsyncSession, user_id: str):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()

async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 10, org_id: str = None):
    stmt = (
        select(User)
        .options(selectinload(User.role), selectinload(User.department))
        .where(User.organization_id == org_id)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_user_in_db(
    db: AsyncSession,
    first_name: str,
    last_name: str,
    email: str,
    hashed_password: str,
    role_id: str,
    department_id: str,
    organization_id: str  
):
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password,
        role_id=role_id,
        department_id=department_id,
        organization_id=organization_id  
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    print(f"New user created with department_id: {new_user.department_id}")
    return new_user


async def update_user_in_db(db: AsyncSession, user_id: str, new_data: UserUpdate, role=None, department=None):
    user = await get_user_by_id(db, user_id)
    if not user:
        return None

    if new_data.first_name is not None:
        user.first_name = new_data.first_name
    if new_data.last_name is not None:
        user.last_name = new_data.last_name
    if new_data.email is not None:
        user.email = new_data.email
    if role:
        user.role_id = role.id
    if department:
        user.department_id = department.id

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user_from_db(db: AsyncSession, user_id: str):
    user = await get_user_by_id(db, user_id)
    if user:
        await db.delete(user)
        await db.commit()
    return user
