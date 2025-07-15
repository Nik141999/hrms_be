from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from src.service import time_tracker_service, break_log_service, work_log_service
from src.schemas.time_tracker_schema import TimeTrackerCreate, TimeTrackerUpdate
from src.schemas.work_log_schema import WorkLogCreate


async def toggle_punch(db: AsyncSession, user_id: str, action: str = "toggle"):
    now = datetime.utcnow()

    # Check if user has an active session
    active_entry = await time_tracker_service.get_active_entry(db, user_id)

    # 1. PUNCH IN (no active session exists)
    if not active_entry:
        create_data = TimeTrackerCreate(
            user_id=user_id,
            punch_in=now,
            punch_out=None,
            duration=None,
            activity=None,
            break_start=None,
            total_break_duration="00:00:00"
        )
        return await time_tracker_service.create_time_tracker(db, create_data)

    # 2. PUNCH OUT
    if action == "punchout":
        # If user is on a break, end it before punching out
        if active_entry.break_start:
            break_duration = now - active_entry.break_start

            await break_log_service.end_break(
                db,
                tracker_id=active_entry.id,
                start=active_entry.break_start,
                end=now
            )

            # Update break duration in TimeTracker
            h, m, s = map(int, (active_entry.total_break_duration or "00:00:00").split(":"))
            total_so_far = timedelta(hours=h, minutes=m, seconds=s)
            new_total = total_so_far + break_duration

            active_entry.break_start = None
            active_entry.total_break_duration = str(new_total).split(".")[0]
            await db.commit()
            await db.refresh(active_entry)

        # Create work log for the current session (up to now)
        await create_work_log_entry(
            db=db,
            time_tracker_id=active_entry.id,
            user_id=user_id,
            start_time=active_entry.punch_in,
            end_time=now,
            total_break_str=active_entry.total_break_duration
        )

        # Calculate total work duration from WorkLog
        total_work_duration = await time_tracker_service.get_total_work_duration(db, active_entry.id)

        # Update time tracker with final punch out and total work time
        update_data = TimeTrackerUpdate(
            punch_out=now,
            duration=str(total_work_duration).split(".")[0],
            break_start=None,
            total_break_duration=active_entry.total_break_duration
        )
        return await time_tracker_service.update_time_tracker(db, active_entry.id, update_data)

    # 3. END BREAK
    if active_entry.break_start:
        break_duration = now - active_entry.break_start

        await break_log_service.end_break(
            db,
            tracker_id=active_entry.id,
            start=active_entry.break_start,
            end=now
        )

        h, m, s = map(int, (active_entry.total_break_duration or "00:00:00").split(":"))
        total_so_far = timedelta(hours=h, minutes=m, seconds=s)
        new_total = total_so_far + break_duration

        update_data = TimeTrackerUpdate(
            break_start=None,
            total_break_duration=str(new_total).split(".")[0]
        )
        return await time_tracker_service.update_time_tracker(db, active_entry.id, update_data)

    # 4. START BREAK (if not on break, treat as starting one)
    await create_work_log_entry(
        db=db,
        time_tracker_id=active_entry.id,
        user_id=user_id,
        start_time=active_entry.punch_in,
        end_time=now,
        total_break_str=active_entry.total_break_duration
    )

    update_data = TimeTrackerUpdate(break_start=now)
    return await time_tracker_service.update_time_tracker(db, active_entry.id, update_data)


async def create_work_log_entry(
    db: AsyncSession,
    time_tracker_id: str,
    user_id: str,
    start_time: datetime,
    end_time: datetime,
    total_break_str: str
):
    h, m, s = map(int, (total_break_str or "00:00:00").split(":"))
    break_duration = timedelta(hours=h, minutes=m, seconds=s)
    actual_duration = end_time - start_time - break_duration

    work_log = WorkLogCreate(
        time_tracker_id=time_tracker_id,
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
        duration=str(actual_duration).split(".")[0]
    )
    await work_log_service.create_work_log(db, work_log)
