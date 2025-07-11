from typing import Optional, Dict
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from src.models.user import User
from src.models.organization import Organization
from src.database import get_db
from src import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"

oauth2_scheme = APIKeyHeader(name="Authorization")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def create_access_token(data: Dict[str, str], expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def create_refresh_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire

async def authenticate_user(db: AsyncSession, email: str, password: str):
    # Check User
    result = await db.execute(
        select(User).options(selectinload(User.role)).where(User.email == email)
    )
    user = result.scalars().first()
    if user and verify_password(password, user.password):
        return user

    # Check Organization
    result = await db.execute(
        select(Organization).options(selectinload(Organization.role), selectinload(Organization.organization_type)).where(Organization.email == email)
    )
    organization = result.scalars().first()
    if organization and verify_password(password, organization.password):
        return organization

    return False


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        if token.startswith("Bearer "):
            token = token[len("Bearer "):]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # ✅ Eager load role
    result = await db.execute(
        select(User).options(selectinload(User.role)).where(User.email == email)
    )
    user = result.scalars().first()
    if user:
        return user

    # fallback to organization
    result = await db.execute(
        select(Organization).where(Organization.email == email)
    )
    organization = result.scalars().first()
    if organization:
        return organization

    raise credentials_exception