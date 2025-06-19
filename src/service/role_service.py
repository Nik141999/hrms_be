from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.role import Role
from src.schemas.roles_schema import RoleCreate, RoleUpdate

class RoleService:
    async def get_all_roles(self, db: AsyncSession):
        result = await db.execute(select(Role))
        return result.scalars().all()

    async def get_role_by_id(self, db: AsyncSession, role_id: int):
        result = await db.execute(select(Role).where(Role.id == role_id))
        return result.scalar_one_or_none()

    async def create_role(self, db: AsyncSession, role_data: RoleCreate):
        new_role = Role(**role_data.dict())
        db.add(new_role)
        await db.commit()
        await db.refresh(new_role)
        return new_role

    async def update_role(self, db: AsyncSession, role_id: int, role_data: RoleUpdate):
        result = await db.execute(select(Role).where(Role.id == role_id))
        role = result.scalar_one_or_none()
        if role:
            for key, value in role_data.dict().items():
                setattr(role, key, value)
            await db.commit()
            await db.refresh(role)
        return role
