from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.controller.org_type_controller import *
from src.schemas.org_type_schema import *

router = APIRouter(prefix="/organization-types", tags=["Organization Type"])

@router.post("/", response_model=OrganizationTypeResponse)
async def create_organization_type(data: OrganizationTypeCreate, db: AsyncSession = Depends(get_db)):
    return await create_organization_type_controller(db, data.org_type)

@router.get("/", response_model=list[OrganizationTypeResponse])
async def get_all_organization_types(db: AsyncSession = Depends(get_db)):
    return await get_all_organization_types_controller(db)

@router.get("/{org_type_id}", response_model=OrganizationTypeResponse)
async def get_organization_type_by_id(org_type_id: str, db: AsyncSession = Depends(get_db)):
    return await get_organization_type_by_id_controller(db, org_type_id)

@router.put("/{org_type_id}", response_model=OrganizationTypeResponse)
async def update_organization_type(org_type_id: str, data: OrganizationTypeUpdate, db: AsyncSession = Depends(get_db)):
    return await update_organization_type_controller(db, org_type_id, data.org_type)

@router.delete("/{org_type_id}")
async def delete_organization_type(org_type_id: str, db: AsyncSession = Depends(get_db)):
    return await delete_organization_type_controller(db, org_type_id)
