from sqlalchemy.ext.asyncio import AsyncSession
from src.models.breakLog import BreakLog

async def end_break(db: AsyncSession, tracker_id: str, start, end):
    break_log = BreakLog(
        time_tracker_id=tracker_id,
        break_start=start,
        break_end=end
    )
    db.add(break_log)
    await db.commit()
    await db.refresh(break_log)
    return break_log
