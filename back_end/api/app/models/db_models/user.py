from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func



# Role Enum
class Role(str, Enum):
    admin = "admin"
    normal = "user"
    paid = "paid_user"
    owner = "owner"

# Base User Model
class UserBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, unique=True, index=True)
    username: Optional[str] = Field(
        default=None,
        unique=True,
        index=True,
        nullable=True,
    )

# Database Model
class User(UserBase, table=True):
    __tablename__ = "users"

    hashed_password: str = Field(nullable=False)
    role: Role = Field(default=Role.normal)
    # Security / Account State
    email_verified: bool = Field(default=False)
    email_verified_at: Optional[datetime] = None
    two_factor_enabled: bool = Field(default=False)
    # Soft delete
    is_active: bool = Field(default=True)
    deleted_at: Optional[datetime] = None
    # Audit timestamps
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )
    )
    # One-to-one Profile relationship
    profile: Optional["Profile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False}
    )
