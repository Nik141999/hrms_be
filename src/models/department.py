from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.utils.utils import generate_uuid
from src.database import Base

class Department(Base):
    __tablename__ = 'departments'

    id = Column(VARCHAR(512), primary_key=True, default=generate_uuid)
    department_name = Column(String(100), nullable=False, unique=True)
    organization_id = Column(VARCHAR(512), ForeignKey("organizations.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="department", lazy="selectin")    
    organization = relationship("Organization", back_populates="departments", lazy="selectin")
