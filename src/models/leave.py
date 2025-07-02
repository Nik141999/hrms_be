from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.utils.utils import generate_uuid
from src.database import Base
from src.enums.leave_enums import LeaveStatus, LeaveType

class Leave(Base):
    __tablename__ = 'leaves'

    id = Column(VARCHAR(512), primary_key=True, default=generate_uuid)
    user_id = Column(VARCHAR(512), ForeignKey("users.id"), nullable=False)
    reviewer_id = Column(VARCHAR(512), ForeignKey("users.id"), nullable=True)
    manager_id = Column(VARCHAR(512), ForeignKey("users.id"), nullable=True)
    
    leave_type = Column(String(50), nullable=False,default=LeaveType.SICK)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(SqlEnum(LeaveStatus), nullable=False, default=LeaveStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="leaves", foreign_keys=[user_id], lazy="selectin")
    reviewer = relationship("User", back_populates="assigned_leaves",foreign_keys=[reviewer_id], lazy="selectin")
    manager = relationship("User", back_populates="managed_leaves", foreign_keys=[manager_id], lazy="selectin")

    