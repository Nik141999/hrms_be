from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TimeTrackerBase(BaseModel):
    user_id: str
    punch_in: Optional[datetime]
    punch_out: Optional[datetime]
    duration: Optional[str]
    activity: Optional[str]
    break_start: Optional[datetime]
    total_break_duration: Optional[str]
    resume_time: Optional[datetime]  # NEW

class TimeTrackerCreate(TimeTrackerBase):
    pass

class TimeTrackerUpdate(BaseModel):
    punch_out: Optional[datetime] = None
    duration: Optional[str] = None
    break_start: Optional[datetime] = None
    total_break_duration: Optional[str] = None
    resume_time: Optional[datetime] = None  # NEW

    class Config:
        orm_mode = True

class TimeTrackerOut(TimeTrackerBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
