from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TimeTrackerBase(BaseModel):
    user_id: str
    punch_in: Optional[datetime]
    punch_out: Optional[datetime]
    duration: Optional[str]
    activity: Optional[str]

class TimeTrackerCreate(TimeTrackerBase):
    pass

class TimeTrackerUpdate(BaseModel):
    punch_out: Optional[datetime]
    duration: Optional[str]

class TimeTrackerOut(TimeTrackerBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
