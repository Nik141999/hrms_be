from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.orgatization_type import OrganizationType

async def create_organization_type_dao(db: AsyncSession, org_type: str) -> OrganizationType:
    new_org_type = OrganizationType(org_type=org_type)
    db.add(new_org_type)
    await db.commit()
    await db.refresh(new_org_type)
    return new_org_type

async def get_all_organization_types_dao(db: AsyncSession, offset: int, limit: int):
    total_result = await db.execute(select(OrganizationType))
    total_items = len(total_result.scalars().all())

    result = await db.execute(select(OrganizationType).offset(offset).limit(limit))
    organization_types = result.scalars().all()
    return total_items, organization_types

async def get_organization_type_by_id_dao(db: AsyncSession, org_type_id: str) -> OrganizationType:
    result = await db.execute(select(OrganizationType).where(OrganizationType.id == org_type_id))
    return result.scalar_one_or_none()

async def update_organization_type_dao(db: AsyncSession, org_type_id: str, new_type: str) -> OrganizationType:
    org_type = await get_organization_type_by_id_dao(db, org_type_id)
    if org_type:
        org_type.org_type = new_type
        await db.commit()
        await db.refresh(org_type)
    return org_type

async def delete_organization_type_dao(db: AsyncSession, org_type_id: str) -> bool:
    org_type = await get_organization_type_by_id_dao(db, org_type_id)
    if org_type:
        await db.delete(org_type)
        await db.commit()
        return True
    return False
