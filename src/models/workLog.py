from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR
from datetime import datetime
from src.database import Base
from src.utils.utils import generate_uuid

class WorkLog(Base):
    __tablename__ = "work_logs"

    id = Column(VARCHAR(512), primary_key=True, default=generate_uuid)
    time_tracker_id = Column(VARCHAR(512), ForeignKey("TimeTracker.id"), nullable=False)    
    user_id = Column(VARCHAR(512), ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    duration = Column(String(20), nullable=False)

    time_tracker = relationship("TimeTracker", back_populates="work_logs",lazy="selectin")
    user = relationship("User", back_populates="work_logs", lazy="selectin")
    
