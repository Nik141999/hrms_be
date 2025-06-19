from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.utils.utils import generate_uuid
from src.database import Base

class OrganizationType(Base):
    __tablename__ = 'organization_type'

    id = Column(VARCHAR(512), primary_key=True, default=generate_uuid)
    org_type = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now()) 
    
    organizations = relationship("Organization", back_populates="organization_type", lazy="selectin") 
    

