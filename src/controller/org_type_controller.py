from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.service.org_type_service import *

async def create_organization_type_controller(db: AsyncSession, org_type: str):
    return await create_organization_type_service(db, org_type)

async def get_all_organization_types_controller(db: AsyncSession, page: int, limit: int):
    return await get_all_organization_types_service(db, page, limit)

async def get_organization_type_by_id_controller(db: AsyncSession, org_type_id: str):
    org_type = await get_organization_type_by_id_service(db, org_type_id)
    if not org_type:
        raise HTTPException(status_code=404, detail="Organization Type not found")
    return org_type

async def update_organization_type_controller(db: AsyncSession, org_type_id: str, new_type: str):
    updated = await update_organization_type_service(db, org_type_id, new_type)
    if not updated:
        raise HTTPException(status_code=404, detail="Organization Type not found")
    return updated

async def delete_organization_type_controller(db: AsyncSession, org_type_id: str):
    deleted = await delete_organization_type_service(db, org_type_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Organization Type not found")
    return {"detail": "Deleted successfully"}
