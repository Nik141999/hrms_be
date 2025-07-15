# src/service/work_log_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.workLog import WorkLog
from src.schemas.work_log_schema import WorkLogCreate
from uuid import uuid4

async def create_work_log(db: AsyncSession, data: WorkLogCreate):
    db_obj = WorkLog(
        id=str(uuid4()),
        **data.dict()
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
