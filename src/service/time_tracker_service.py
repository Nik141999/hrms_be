from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.time_tracker_schema import TimeTrackerCreate, TimeTrackerUpdate
from src.dao import time_tracker_dao

async def create(db: AsyncSession, data: TimeTrackerCreate):
    return await time_tracker_dao.create_time_tracker(db, data)

async def update(db: AsyncSession, tracker_id: str, data: TimeTrackerUpdate):
    return await time_tracker_dao.update_time_tracker(db, tracker_id, data)

async def get_active_entry(db: AsyncSession, user_id: str):
    return await time_tracker_dao.get_active_entry(db, user_id)
