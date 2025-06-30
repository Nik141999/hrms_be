from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import (
    UserLogin, UserLoginResponse, OrgLoginResponse,
    UserResponse, OrgResponse
)
from src.models.user import User
from src.models.organization import Organization
from src.utils.auth import authenticate_user, create_access_token, create_refresh_token
from src.database import get_db

router = APIRouter(tags=["authentication"])

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
