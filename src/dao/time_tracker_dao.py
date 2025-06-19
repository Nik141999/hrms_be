from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.time_tracker import TimeTracker
from src.schemas.time_tracker_schema import TimeTrackerCreate, TimeTrackerUpdate

async def create_time_tracker(db: AsyncSession, time_tracker: TimeTrackerCreate):
    db_obj = TimeTracker(**time_tracker.dict())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def update_time_tracker(db: AsyncSession, tracker_id: str, updates: TimeTrackerUpdate):
    stmt = select(TimeTracker).where(TimeTracker.id == tracker_id)
    result = await db.execute(stmt)
    db_obj = result.scalars().first()
    if db_obj:
        for key, value in updates.dict(exclude_unset=True).items():
            setattr(db_obj, key, value)
        await db.commit()
        await db.refresh(db_obj)
    return db_obj

async def get_active_entry(db: AsyncSession, user_id: str):
    stmt = (
        select(TimeTracker)
        .where(TimeTracker.user_id == user_id, TimeTracker.punch_out == None)
        .order_by(TimeTracker.punch_in.desc())
        .limit(1)
    )
    result = await db.execute(stmt)
    return result.scalars().first()
