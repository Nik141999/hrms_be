from sqlalchemy import Column, String, Boolean,DateTime,ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.utils.utils import generate_uuid
from src.database import Base
from src.models.role import Role
 

class User(Base):
    __tablename__ = 'users'

    id = Column(VARCHAR(512), primary_key=True, default=generate_uuid)
    role_id = Column(VARCHAR(512), ForeignKey("roles.id"), nullable=False)
    organization_id = Column(VARCHAR(512), ForeignKey("organizations.id"), nullable=True)
    department_id = Column(VARCHAR(512), ForeignKey("departments.id"), nullable=True)

    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    email = Column(String(90), unique=True, index=True)
    password = Column(String(255), nullable=False) 
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


    role = relationship("Role", back_populates="user", lazy="selectin")
    organization = relationship("Organization", back_populates="user", lazy="selectin")
    department = relationship("Department", back_populates="user", lazy="selectin")

    leaves = relationship(
        "Leave",
        back_populates="user",
        foreign_keys="Leave.user_id",
        lazy="selectin"
    )

    assigned_leaves = relationship(
        "Leave",
        back_populates="reviewer",
        foreign_keys="Leave.reviewer_id",
        lazy="selectin"
    )
    
    time_tracker = relationship(
    "TimeTracker",
    back_populates="user",
    lazy="selectin",
    )
    
    managed_leaves = relationship(
        "Leave",
        back_populates="manager",
        foreign_keys="Leave.manager_id",
        lazy="selectin"
    )

    