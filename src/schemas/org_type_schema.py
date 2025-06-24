from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

class OrganizationTypeCreate(BaseModel):
    org_type: str

class OrganizationTypeUpdate(BaseModel):
    org_type: str

class OrganizationTypeResponse(BaseModel):
    id: str
    org_type: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)  
class PaginatedOrganizationTypeResponse(BaseModel):
    totalItems: int
    totalPages: int
    currentPage: int
    pageSize: int
    organization_types: List[OrganizationTypeResponse]
