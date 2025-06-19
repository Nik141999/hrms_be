from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey,Integer
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.utils.utils import generate_uuid
from src.database import Base
from src.models.orgatization_type import OrganizationType

class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(VARCHAR(512), primary_key=True, default=generate_uuid)
    org_name = Column(String(100), nullable=False, unique=True)
    email = Column(String(90), unique=True, index=True)
    password = Column(String(255), nullable=False) 
    address = Column(String(255), nullable=True)
    phone_number = Column(VARCHAR(20), nullable=True)
    description = Column(String(500), nullable=True)
    website = Column(String(255), nullable=True)
    gst_number = Column(VARCHAR(40), nullable=True)
    is_active = Column(Boolean, default=True)
    otp = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    role_id = Column(VARCHAR(512), ForeignKey("roles.id"), nullable=False)
    
    org_type_id = Column(VARCHAR(512), ForeignKey("organization_type.id"), nullable=True)
    
    user = relationship("User", back_populates="organization", lazy="selectin")
    role = relationship("Role", back_populates="organizations", lazy="selectin")
    organization_type = relationship(
        OrganizationType,  
        back_populates="organizations",
        lazy="selectin"
    )

