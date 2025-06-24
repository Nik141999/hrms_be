from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.org_type_dao import (
    create_organization_type_dao, get_all_organization_types_dao,
    get_organization_type_by_id_dao, update_organization_type_dao,
    delete_organization_type_dao
)

async def create_organization_type_service(db: AsyncSession, org_type: str):
    return await create_organization_type_dao(db, org_type)

async def get_all_organization_types_service(db: AsyncSession, page: int, limit: int):
    offset = (page - 1) * limit
    total_items, items = await get_all_organization_types_dao(db, offset, limit)

    return {
        "totalItems": total_items,
        "totalPages": (total_items + limit - 1) // limit,
        "currentPage": page,
        "pageSize": limit,
        "organization_types": items,
    }

async def get_organization_type_by_id_service(db: AsyncSession, org_type_id: str):
    return await get_organization_type_by_id_dao(db, org_type_id)

async def update_organization_type_service(db: AsyncSession, org_type_id: str, new_type: str):
    return await update_organization_type_dao(db, org_type_id, new_type)

async def delete_organization_type_service(db: AsyncSession, org_type_id: str):
    return await delete_organization_type_dao(db, org_type_id)
