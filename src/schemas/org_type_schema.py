from pydantic import BaseModel
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

    class Config:
        orm_mode = True
