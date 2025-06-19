from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.time_tracker_schema import TimeTrackerCreate, TimeTrackerUpdate
from src.service import time_tracker_service

async def toggle_punch(db: AsyncSession, user_id: str):
    active_entry = await time_tracker_service.get_active_entry(db, user_id)

    if active_entry:
        now = datetime.utcnow()
        punch_in_time = active_entry.punch_in
        duration = str(now - punch_in_time).split('.')[0]

        update_data = TimeTrackerUpdate(
            punch_out=now,
            duration=duration
        )
        return await time_tracker_service.update(db, active_entry.id, update_data)
    else:
        create_data = TimeTrackerCreate(
            user_id=user_id,
            punch_in=datetime.utcnow(),
            punch_out=None,
            duration=None,
            activity=None
        )
        return await time_tracker_service.create(db, create_data)
