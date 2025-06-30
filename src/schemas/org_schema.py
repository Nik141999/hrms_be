from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, List
from datetime import datetime

class OrgCreate(BaseModel):
    org_name: str
    email: EmailStr
    password: str
    role_type: Optional[str] = "SuperAdmin"  # ✅ Default to SuperAdmin

    address: Optional[str] = None
    phone_number: Optional[str] = None
    organization_type: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    gst_number: Optional[str] = None

class OrgUpdate(BaseModel):
    org_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    organization_type: Optional[str] = None
    role_type: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    gst_number: Optional[str] = None

class OrgResponse(BaseModel):
    id: str
    org_name: str
    email: EmailStr                    
    role_type: Optional[str] = None     
    address: Optional[str] = None
    phone_number: Optional[str] = None
    organization_type: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    gst_number: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str

class PaginatedOrgResponse(BaseModel):
    totalItems: int
    totalPages: int
    currentPage: int
    pageSize: int
    organizations: List[OrgResponse]
