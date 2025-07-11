from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.schemas.user import (
    UserLogin, UserLoginResponse, OrgLoginResponse,
    UserResponse, OrgResponse,
    TokenRefreshRequest, TokenRefreshResponse
)
from src.models.user import User
from src.models.organization import Organization
from src.utils.auth import (
    authenticate_user, create_access_token,
    create_refresh_token
)
from src.database import get_db
from src import config

router = APIRouter(tags=["authentication"])
SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"

# ------------------- LOGIN -------------------

@router.post("/login")
async def login_user(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    authenticated = await authenticate_user(
        db=db,
        email=login_data.email,
        password=login_data.password
    )

    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token_expires = timedelta(minutes=960)
    refresh_token_expires = timedelta(days=30)

    # User login
    if isinstance(authenticated, User):
        role_type = authenticated.role.role_type if authenticated.role else None
        department_name = authenticated.department.department_name if authenticated.department else None

        access_token = await create_access_token(
            data={
                "sub": authenticated.email,
                "role_type": role_type,
                "org_id": authenticated.organization_id,
            },
            expires_delta=access_token_expires
        )
        refresh_token, _ = await create_refresh_token(
            data={
                "sub": authenticated.email,
                "role_type": role_type,
                "org_id": authenticated.organization_id,
            },
            expires_delta=refresh_token_expires
        )

        response_data = UserLoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            role_type=role_type,
            user=UserResponse(
                id=authenticated.id,
                first_name=authenticated.first_name,
                last_name=authenticated.last_name,
                email=authenticated.email,
                role_type=role_type,
                department_name=department_name
            )
        )
        return JSONResponse(content=response_data.model_dump())

    # Organization login
    elif isinstance(authenticated, Organization):
        role_type = authenticated.role.role_type if authenticated.role else "Organization"

        access_token = await create_access_token(
            data={
                "sub": authenticated.email,
                "role_type": role_type,
                "org_id": authenticated.id,
            },
            expires_delta=access_token_expires
        )
        refresh_token, _ = await create_refresh_token(
            data={
                "sub": authenticated.email,
                "role_type": role_type,
                "org_id": authenticated.id,
            },
            expires_delta=refresh_token_expires
        )

        response_data = OrgLoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            role_type=role_type,
            organization=OrgResponse(
                id=authenticated.id,
                org_name=authenticated.org_name,
                email=authenticated.email,
                address=authenticated.address,
                phone_number=authenticated.phone_number,
                organization_type=authenticated.organization_type.org_type if authenticated.organization_type else None,
                description=authenticated.description,
                website=authenticated.website,
                gst_number=authenticated.gst_number
            )
        )
        return JSONResponse(content=response_data.model_dump())

# ------------------- REFRESH TOKEN -------------------

@router.post("/refresh-token", response_model=TokenRefreshResponse)
async def refresh_token(
    token_request: TokenRefreshRequest,
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token_request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        role_type = payload.get("role_type")
        org_id = payload.get("org_id")

        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Check if user or organization still exists
    result = await db.execute(
        select(User).options(selectinload(User.role)).where(User.email == email)
    )
    user = result.scalars().first()

    if user:
        identity = user
    else:
        result = await db.execute(
            select(Organization).where(Organization.email == email)
        )
        organization = result.scalars().first()
        if not organization:
            raise credentials_exception
        identity = organization

    # Create new tokens
    access_token_expires = timedelta(minutes=960)
    refresh_token_expires = timedelta(days=30)

    access_token = await create_access_token(
        data={"sub": email, "role_type": role_type, "org_id": org_id},
        expires_delta=access_token_expires
    )
    refresh_token, _ = await create_refresh_token(
        data={"sub": email, "role_type": role_type, "org_id": org_id},
        expires_delta=refresh_token_expires
    )

    return TokenRefreshResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )
