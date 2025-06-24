from pydantic import BaseModel
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class DepartmentCreate(BaseModel):
    department_name: str
    
    
class DepartmentUpdate(BaseModel):
    department_name: Optional[str] = None

class DepartmentResponse(BaseModel):
    id: str
    department_name: str

    model_config = ConfigDict(from_attributes=True)    

class PaginatedDepartmentResponse(BaseModel):
    totalItems: int
    totalPages: int
    currentPage: int
    pageSize: int
    departments: List[DepartmentResponse]        