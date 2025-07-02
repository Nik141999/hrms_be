from pydantic import BaseModel, EmailStr, ConfigDict, model_validator
from typing import Optional, List
from datetime import datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    role_type: str
    department_name: Optional[str] = None

    @model_validator(mode="after")
    def validate_department_for_non_admin(self) -> 'UserCreate':
        if self.role_type.lower() != "admin" and not self.department_name:
            raise ValueError("department_name is required for non-admin users")
        return self

class UserResponse(BaseModel):
    id: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    role_type: Optional[str]
    department_name: Optional[str]

    model_config = ConfigDict(from_attributes=True)
    
class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    role_type: Optional[str]
    department_name: Optional[str]
class OrgResponse(BaseModel):
    id: str
    org_name: str
    email: str
    address: Optional[str] = None
    phone_number: Optional[str] = None
    organization_type: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    gst_number: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    role_type: str
    user: UserResponse

class OrgLoginResponse(BaseModel):
    access_token: str
    refresh_token: str 
    token_type: str
    role_type: str
    organization: OrgResponse
    
    
class PaginatedUserResponse(BaseModel):
    totalItems: int
    totalPages: int
    currentPage: int
    pageSize: int
    users: List[UserResponse]    
