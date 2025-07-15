from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.controller import time_tracker_controller
from src.schemas.time_tracker_schema import TimeTrackerOut
from src.utils.auth import get_current_user
from src.models.user import User

router = APIRouter(prefix="/time-tracker", tags=["TimeTracker"])

@router.post("/toggle", response_model=TimeTrackerOut)
async def toggle(
    action: str = Query("toggle", enum=["toggle", "punchout"]),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await time_tracker_controller.toggle_punch(db, current_user.id, action)
