from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class PermissionActions(BaseModel):
    edit: bool = False
    view: bool = False  
    create: bool = False
    delete: bool = False


class RoutePermission(BaseModel):
    route: str
    permission: PermissionActions


class RoleBase(BaseModel):
    role_type: str = Field(..., example="Admin")  # changed role_name to role_type
    permission: Optional[List[RoutePermission]] = Field(default_factory=list)


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    role_type: Optional[str] = None  # changed role_name to role_type
    permission: Optional[List[RoutePermission]] = None


class RoleOut(RoleBase):
    id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
