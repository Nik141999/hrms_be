from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.utils.utils import generate_uuid
from src.database import Base

class Role(Base):
    __tablename__ = 'roles'

    id = Column(VARCHAR(512), primary_key=True, default=generate_uuid)
    role_type = Column(String(50), unique=True, index=True, nullable=False)
    permission = Column(JSON, nullable=True)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  

    user = relationship("User", back_populates="role")
    organizations = relationship("Organization", back_populates="role", lazy="selectin")
    
