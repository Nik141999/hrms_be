from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from src.dao.org_dao import *
from src.dao.user_dao import get_user_by_email
from src.schemas.org_schema import OrgCreate, OrgUpdate, OrgResponse, PaginatedOrgResponse
from src.utils.auth import get_hash_password

async def create_org_service(org: OrgCreate, db: AsyncSession) -> OrgResponse:
    if await get_org_by_email(db, org.email):
        raise ValueError("Email already registered")

    if await get_user_by_email(db, org.email):
        raise ValueError("Email already registered as a user")

    # ✅ Use default if role_type is None
    role_type = org.role_type or "SuperAdmin"

    role = await get_role_by_name(db, role_type)
    if not role:
        raise ValueError("Invalid role_type")

    org_type = await get_org_type_by_name(db, org.organization_type) if org.organization_type else None
    if org.organization_type and not org_type:
        raise ValueError("Invalid organization_type")

    hashed_password = get_hash_password(org.password)

    new_org = await create_org_in_db(
        db=db,
        org_name=org.org_name,
        email=org.email,
        hashed_password=hashed_password,
        role_id=role.id,
        address=org.address,
        phone_number=org.phone_number,
        org_type_id=org_type.id if org_type else None,
        description=org.description,
        website=org.website,
        gst_number=org.gst_number,
    )

    await db.refresh(new_org, attribute_names=["organization_type"])

    return OrgResponse(
    id=new_org.id,
    org_name=new_org.org_name,
    email=new_org.email,                       
    role_type=new_org.role.role_type if new_org.role else None,  
    address=new_org.address,
    phone_number=new_org.phone_number,
    organization_type=new_org.organization_type.org_type if new_org.organization_type else None,
    description=new_org.description,
    website=new_org.website,
    gst_number=new_org.gst_number,
)




async def get_all_org_service(db: AsyncSession, page: int, limit: int, search: str = None) -> PaginatedOrgResponse:
    base_query = select(func.count()).select_from(Organization)

    if search:
        search_pattern = f"%{search}%"
        base_query = base_query.where(
            or_(
                Organization.org_name.ilike(search_pattern),
                Organization.email.ilike(search_pattern)
            )
        )

    total_items = await db.scalar(base_query)
    offset = (page - 1) * limit

    orgs = await get_all_org(db, skip=offset, limit=limit, search=search)

    org_list = [
        OrgResponse(
            id=org.id,
            org_name=org.org_name,
            email=org.email,
            role_type=org.role.role_type if org.role else None,
            address=org.address,
            phone_number=org.phone_number,
            organization_type=org.organization_type.org_type if org.organization_type else None,
            description=org.description,
            website=org.website,
            gst_number=org.gst_number
        )
        for org in orgs
    ]

    total_pages = (total_items + limit - 1) // limit

    return PaginatedOrgResponse(
        totalItems=total_items,
        totalPages=total_pages,
        currentPage=page,
        pageSize=limit,
        organizations=org_list
    )
    
async def get_org_by_id_service(org_id: str, db: AsyncSession) -> OrgResponse:
    org = await get_org_by_id(db, org_id)
    if not org:
        raise ValueError("Organization not found")

    return OrgResponse(
        id=org.id,
        org_name=org.org_name,
        is_active=org.is_active,
        created_at=org.created_at,
        address=org.address,
        phone_number=org.phone_number,
        organization_type=org.organization_type.org_type if org.organization_type else None,
        description=org.description,
        website=org.website,
        gst_number=org.gst_number
    )
    


async def update_org_service(org_id: str, org_data: OrgUpdate, db: AsyncSession) -> OrgResponse:
    update_dict = org_data.dict(exclude_unset=True)
    if "password" in update_dict:
        update_dict["password"] = get_hash_password(update_dict["password"])

    org = await update_org_in_db(db, org_id, update_dict)
    if not org:
        raise ValueError("Organization not found")

    return OrgResponse(
        id=org.id,
        org_name=org.org_name,
        is_active=org.is_active,
        created_at=org.created_at,
        address=org.address,
        phone_number=org.phone_number,
        organization_type=org.organization_type.org_type if org.organization_type else None,
        description=org.description,
        website=org.website,
        gst_number=org.gst_number
    )


async def delete_org_service(org_id: str, db: AsyncSession):
    org = await delete_org_from_db(db, org_id)
    if not org:
        raise ValueError("Organization not found")
    return {"detail": "Organization deleted successfully"}


async def verify_org_otp_service(email: str, otp: str, db: AsyncSession):
    org = await get_org_by_email_from_organization(db, email)
    if not org:
        raise ValueError("Organization not found")

    # ✅ Validate OTP presence and expiry
    if not org.otp or not org.otp_expiry:
        raise ValueError("OTP already used.")

    if datetime.utcnow() > org.otp_expiry:
        raise ValueError("OTP has expired.")

    if str(org.otp).strip() != str(otp).strip():
        raise ValueError("Invalid OTP.")

    # ✅ Clear OTP and activate organization
    org.otp = None
    org.otp_expiry = None
    org.is_active = True
    await db.commit()
    await db.refresh(org)

    return {"detail": "OTP verified successfully"}