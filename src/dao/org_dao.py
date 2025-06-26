from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.organization import Organization
from src.models.orgatization_type import OrganizationType
from src.models.role import Role
from src.models.user import User
from datetime import datetime, timedelta
from src.utils.utils import generate_otp
from src.utils.email_sender import send_otp_email

async def get_role_by_name(db: AsyncSession, role_type: str):
    result = await db.execute(select(Role).where(Role.role_type == role_type.lower()))
    return result.scalars().first()


async def get_org_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalars().first()

async def get_org_type_by_name(db: AsyncSession, org_type_name: str):
    result = await db.execute(
        select(OrganizationType).where(OrganizationType.org_type.ilike(org_type_name))

    )
    return result.scalars().first()

async def get_org_by_id(db: AsyncSession, org_id: str):
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    return result.scalars().first()

async def get_all_org(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Organization).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def create_org_in_db(
    db: AsyncSession,
    org_name: str,
    email: str,
    hashed_password: str,
    role_id: str,
    address: str = None,
    phone_number: str = None,
    org_type_id: str = None,
    description: str = None,
    website: str = None,
    gst_number: str = None,
):
    # Check for duplicate org name
    result = await db.execute(select(Organization).where(Organization.org_name == org_name))
    existing_org = result.scalar_one_or_none()
    if existing_org:
        raise ValueError(f"Organization name '{org_name}' already exists.")

    # Check for duplicate GST number
    if gst_number:
        gst_result = await db.execute(select(Organization).where(Organization.gst_number == gst_number))
        existing_gst_org = gst_result.scalars().first()
        if existing_gst_org:
            raise ValueError(f"GST number '{gst_number}' is already registered.")

    # ✅ Generate OTP before using
    otp = generate_otp()
    otp_expiry = datetime.utcnow() + timedelta(minutes=5)

    # Create organization
    new_org = Organization(
        org_name=org_name,
        email=email,
        password=hashed_password,
        role_id=role_id,
        address=address,
        phone_number=phone_number,
        org_type_id=org_type_id,
        description=description,
        website=website,
        gst_number=gst_number,
        otp=otp,
        otp_expiry=otp_expiry
    )

    db.add(new_org)
    await db.commit()
    await db.refresh(new_org)

    # Send OTP email
    send_otp_email(email, otp)

    return new_org


async def update_org_in_db(db: AsyncSession, org_id: str, update_data: dict):
    org = await get_org_by_id(db, org_id)
    if not org:
        return None

    for key, value in update_data.items():
        # Handle relationship: organization_type (expects OrganizationType instance)
        if key == "organization_type":
            org_type_result = await db.execute(
                select(OrganizationType).where(OrganizationType.org_type.ilike(value))
            )
            org_type = org_type_result.scalars().first()
            if not org_type:
                raise ValueError("Invalid organization_type")
            org.organization_type = org_type

        # Handle relationship: role_type (expects Role instance)
        elif key == "role_type":
            role_result = await db.execute(
                select(Role).where(Role.role_type.ilike(value))
            )
            role = role_result.scalars().first()
            if not role:
                raise ValueError("Invalid role_type")
            org.role = role

        # Regular fields (email, password, etc.)
        else:
            setattr(org, key, value)

    await db.commit()
    await db.refresh(org)
    return org

async def delete_org_from_db(db: AsyncSession, org_id: str):
    org = await get_org_by_id(db, org_id)
    if org:
        await db.delete(org)
        await db.commit()
    return org

async def get_org_by_email_from_organization(db: AsyncSession, email: str):
    result = await db.execute(
        select(Organization).where(Organization.email == email)
    )
    return result.scalars().first()
