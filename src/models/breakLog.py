from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.sql import func
from src.utils.utils import generate_uuid
from src.database import Base
from sqlalchemy.orm import relationship

class BreakLog(Base):
    __tablename__ = "BreakLog"

    id = Column(VARCHAR(512), primary_key=True, default=generate_uuid)
    time_tracker_id = Column(VARCHAR(512), ForeignKey("TimeTracker.id"), nullable=False)
    break_start = Column(DateTime(timezone=True), nullable=False)
    break_end = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    time_tracker = relationship("TimeTracker", back_populates="break_logs", lazy="selectin")
