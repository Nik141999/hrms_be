from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from src.enums.leave_enums import LeaveStatus

class LeaveCreate(BaseModel):
    leave_type: str
    description: Optional[str]
    start_date: date
    end_date: date

class LeaveUpdate(BaseModel):
    leave_type: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class LeaveResponse(BaseModel):
    id: str
    user_id: str
    reviewer_id: Optional[str]
    manager_id: Optional[str]
    leave_type: str
    start_date: date
    end_date: date
    description: str
    hr_status: Optional[LeaveStatus]
    manager_status: Optional[LeaveStatus]
    status: LeaveStatus
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class PaginatedLeaveResponse(BaseModel):
    totalItems: int
    totalPages: int
    currentPage: int
    pageSize: int
    leaves: List[LeaveResponse]
