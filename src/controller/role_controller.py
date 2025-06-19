from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.roles_schema import RoleCreate, RoleUpdate
from src.service.role_service import RoleService

class RoleController:
    def __init__(self):
        self.role_service = RoleService()

    async def get_roles(self, db: AsyncSession):
        return await self.role_service.get_all_roles(db)

    async def get_role_by_id(self, db: AsyncSession, role_id: int):
        role = await self.role_service.get_role_by_id(db, role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role

    async def create_role(self, db: AsyncSession, role: RoleCreate):
        return await self.role_service.create_role(db, role)

    async def update_role(self, db: AsyncSession, role_id: int, role: RoleUpdate):
        updated = await self.role_service.update_role(db, role_id, role)
        if not updated:
            raise HTTPException(status_code=404, detail="Role not found")
        return updated
