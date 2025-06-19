from pydantic import BaseModel
from typing import Optional

class DepartmentCreate(BaseModel):
    department_name: str
    
    
class DepartmentUpdate(BaseModel):
    department_name: Optional[str] = None

class DepartmentResponse(BaseModel):
    id: str
    department_name: str

    class Config:
        orm_mode = True    