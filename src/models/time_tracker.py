from sqlalchemy import Column, String, DateTime,ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.utils.utils import generate_uuid
from src.models.user import User
from src.database import Base

class TimeTracker(Base):
    __tablename__ = 'TimeTracker'

    id = Column(VARCHAR(512), primary_key=True, default=generate_uuid)
    user_id = Column(VARCHAR(512),ForeignKey("users.id"), nullable=False)
    punch_in = Column(DateTime(timezone=True), nullable=True)
    punch_out = Column(DateTime(timezone=True), nullable=True)
    duration = Column(String(50), nullable=True)  
    activity = Column(String(255), nullable=True)   
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  
    
    user = relationship("User", back_populates="time_tracker", lazy="selectin")   
