from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from src.service import time_tracker_service, break_log_service, work_log_service
from src.schemas.time_tracker_schema import TimeTrackerCreate, TimeTrackerUpdate
from src.schemas.work_log_schema import WorkLogCreate
from src.utils.time_utils import format_duration
from src.dao import break_log_dao


async def toggle_punch(db: AsyncSession, user_id: str, action: str = "toggle"):
    now = datetime.utcnow()
    active_entry = await time_tracker_service.get_active_entry(db, user_id)

    if action == "toggle":
        if not active_entry:
            create_data = TimeTrackerCreate(
                user_id=user_id,
                punch_in=now,
                punch_out=None,
                duration=None,
                activity=None,
                break_start=None,
                total_break_duration="00:00:00",
                resume_time=now
            )
            return await time_tracker_service.create_time_tracker(db, create_data)
        else:
            raise ValueError("Already punched in. Use 'break' or 'punchout'.")

    elif action == "break":
        if not active_entry:
            raise ValueError("You must punch in before taking a break.")

        if active_entry.break_start:
            # End break
            break_duration = now - active_entry.break_start

            await break_log_service.end_break(
                db, active_entry.id, active_entry.break_start, now
            )

            h, m, s = map(int, (active_entry.total_break_duration or "00:00:00").split(":"))
            total_so_far = timedelta(hours=h, minutes=m, seconds=s)
            new_total = total_so_far + break_duration

            update_data = TimeTrackerUpdate(
                break_start=None,
                total_break_duration=format_duration(new_total),
                resume_time=now
            )
            return await time_tracker_service.update_time_tracker(db, active_entry.id, update_data)

        else:
            # Start break
            await create_work_log_entry(
                db=db,
                time_tracker_id=active_entry.id,
                user_id=user_id,
                start_time=active_entry.resume_time or active_entry.punch_in,
                end_time=now
            )

            update_data = TimeTrackerUpdate(
                break_start=now,
                resume_time=None
            )
            return await time_tracker_service.update_time_tracker(db, active_entry.id, update_data)

    elif action == "punchout":
        if not active_entry:
            raise ValueError("No active session to punch out from.")

        if active_entry.break_start:
            break_duration = now - active_entry.break_start
            await break_log_service.end_break(
                db, active_entry.id, active_entry.break_start, now
            )

            h, m, s = map(int, (active_entry.total_break_duration or "00:00:00").split(":"))
            total_so_far = timedelta(hours=h, minutes=m, seconds=s)
            new_total = total_so_far + break_duration

            active_entry.break_start = None
            active_entry.total_break_duration = format_duration(new_total)
            await db.commit()
            await db.refresh(active_entry)

        # Log final work session
        await create_work_log_entry(
            db=db,
            time_tracker_id=active_entry.id,
            user_id=user_id,
            start_time=active_entry.resume_time or active_entry.punch_in,
            end_time=now
        )

        total_work_duration = await time_tracker_service.get_total_work_duration(db, active_entry.id)

        update_data = TimeTrackerUpdate(
            punch_out=now,
            duration=format_duration(total_work_duration),
            break_start=None,
            total_break_duration=active_entry.total_break_duration,
            resume_time=None
        )
        return await time_tracker_service.update_time_tracker(db, active_entry.id, update_data)

    else:
        raise ValueError("Invalid action. Use 'toggle', 'break', or 'punchout'.")


async def create_work_log_entry(
    db: AsyncSession,
    time_tracker_id: str,
    user_id: str,
    start_time: datetime,
    end_time: datetime,
):
    if not start_time:
        raise ValueError("start_time is required to create work log")

    raw_duration = end_time - start_time
    breaks = await break_log_dao.get_breaks_in_range(db, time_tracker_id, start_time, end_time)
    break_duration = sum((b.end_time - b.start_time for b in breaks), timedelta())

    actual_duration = raw_duration - break_duration
    if actual_duration.total_seconds() < 0:
        actual_duration = timedelta()

    duration_str = format_duration(actual_duration)

    work_log = WorkLogCreate(
        time_tracker_id=time_tracker_id,
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
        duration=duration_str
    )
    await work_log_service.create_work_log(db, work_log)
