from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from src.models.user import User  # Add this import
from src.dao.user_dao import (
    get_user_by_email,
    get_user_by_id,
    create_user_in_db,
    update_user_in_db,
    delete_user_from_db,
    get_all_users,
    get_role_by_name,
    get_department_by_name
)
from src.dao.org_dao import get_org_by_email
from src.schemas.user import UserCreate, UserResponse, UserUpdate, PaginatedUserResponse
from src.utils.auth import get_hash_password
from src.utils.email_sender import send_credentials_email


async def create_user_service(user: UserCreate, db: AsyncSession, org_id: str) -> UserResponse:
    # Check if user already exists
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise ValueError("Email already registered")

    # Check if email is already used for an organization
    existing_org = await get_org_by_email(db, user.email)
    if existing_org:
        raise ValueError("Email already registered as an organization")

    # Fetch role
    role = await get_role_by_name(db, user.role_type)
    if not role:
        raise ValueError("Invalid role_type")

    # Normalize role type
    role_type = role.role_type.lower()

    # Only validate department if role is not 'admin'
    department = None
    if role_type != "admin":
        department = await get_department_by_name(db, user.department_name)
        if not department:
            raise ValueError("Invalid department")

    # Hash the password
    hashed_password = get_hash_password(user.password)

    # Create user
    new_user = await create_user_in_db(
        db=db,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password,
        role_id=role.id,
        department_id=department.id if department else None,
        organization_id=org_id
    )

    # Refresh user to get related role and department
    await db.refresh(new_user, attribute_names=["role", "department"])

    # Send credentials via email
    send_credentials_email(
        to_email=user.email,
        user_email=user.email,
        password=user.password
    )

    # Return response
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        role_type=new_user.role.role_type if new_user.role else None,
        department_name=new_user.department.department_name if new_user.department else None
    )

async def get_user_service(user_id: str, db: AsyncSession) -> UserResponse:
    user = await get_user_by_id(db, user_id)
    if not user:
        raise ValueError("User not found")
    return UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role_type=user.role.role_type if user.role else None,
        department_name=user.department.department_name if user.department else None
    )


async def get_all_users_service(db: AsyncSession, page: int, limit: int, org_id: str, search: str = None) -> PaginatedUserResponse:
    base_query = select(func.count()).select_from(User).where(User.organization_id == org_id)

    if search:
        search_pattern = f"%{search}%"
        base_query = base_query.where(
            or_(
                User.first_name.ilike(search_pattern),
                User.last_name.ilike(search_pattern),
                User.email.ilike(search_pattern)
            )
        )

    total_items = await db.scalar(base_query)
    offset = (page - 1) * limit

    users = await get_all_users(db, skip=offset, limit=limit, org_id=org_id, search=search)
    total_pages = (total_items + limit - 1) // limit

    return PaginatedUserResponse(
        totalItems=total_items,
        totalPages=total_pages,
        currentPage=page,
        pageSize=limit,
        users=[
            UserResponse(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                role_type=user.role.role_type if user.role else None,
                department_name=user.department.department_name if user.department else None
            )
            for user in users
        ]
    )


async def update_user_service(user_id: str, user_update: UserUpdate, db: AsyncSession) -> UserResponse:
    role = None
    department = None

    if user_update.role_type:
        role = await get_role_by_name(db, user_update.role_type)
        if not role:
            raise ValueError("Invalid role_type")

    if user_update.department_name:
        department = await get_department_by_name(db, user_update.department_name)
        if not department:
            raise ValueError("Invalid department_name")

    user = await update_user_in_db(
        db=db,
        user_id=user_id,
        new_data=user_update,
        role=role,
        department=department
    )
    if not user:
        raise ValueError("User not found")

    return UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role_type=user.role.role_type if user.role else None,
        department_name=user.department.department_name if user.department else None
    )


async def delete_user_service(user_id: str, db: AsyncSession):
    user = await delete_user_from_db(db, user_id)
    if not user:
        raise ValueError("User not found")
    return {"detail": "User deleted successfully"}
