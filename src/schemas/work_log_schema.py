from pydantic import BaseModel
from datetime import datetime

class WorkLogCreate(BaseModel):
    time_tracker_id: str
    user_id: str
    start_time: datetime
    end_time: datetime
    duration: str

class WorkLogOut(WorkLogCreate):
    id: str

    class Config:
        orm_mode = True
