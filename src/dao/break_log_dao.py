from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.breakLog import BreakLog


async def get_breaks_in_range(db: AsyncSession, time_tracker_id: str, start_time, end_time):
    stmt = (
        select(BreakLog)
        .where(
            BreakLog.time_tracker_id == time_tracker_id,
            BreakLog.break_start >= start_time,
            BreakLog.break_end <= end_time
        )
    )
    result = await db.execute(stmt)
    return result.scalars().all()
