from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.auth import get_current_user
from src.controller.org_controller import *
from src.schemas.org_schema import OrgCreate, OrgUpdate, OrgResponse
from src.database import get_db

router = APIRouter(tags=["Organization"])

@router.post("/organization", response_model=OrgResponse)
async def create_organization(org: OrgCreate, db: AsyncSession = Depends(get_db)):
    return await create_org_controller(org, db)

@router.get("/organization", response_model=list[OrgResponse])
async def get_organizations(db: AsyncSession = Depends(get_db)):
    return await get_all_org_controller(db)

@router.put("/organization/{org_id}", response_model=OrgResponse)
async def update_organization(org_id: str, org_data: OrgUpdate, db: AsyncSession = Depends(get_db)):
    return await update_org_controller(org_id, org_data, db)

@router.delete("/organization/{org_id}")
async def delete_organization(org_id: str, db: AsyncSession = Depends(get_db)):
    return await delete_org_controller(org_id, db)
