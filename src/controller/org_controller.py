from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.org_schema import OrgCreate, OrgUpdate, OrgResponse
from src.service.org_service import *

async def create_org_controller(org: OrgCreate, db: AsyncSession):
    try:
        return await create_org_service(org, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

async def get_all_org_controller(db: AsyncSession):
    return await get_all_org_service(db)

async def update_org_controller(org_id: str, data: OrgUpdate, db: AsyncSession):
    try:
        return await update_org_service(org_id, data, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

async def delete_org_controller(org_id: str, db: AsyncSession):
    try:
        return await delete_org_service(org_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
async def verify_otp_controller(email: str, otp: str, db: AsyncSession):
    try:
        return await verify_org_otp_service(email, otp, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
