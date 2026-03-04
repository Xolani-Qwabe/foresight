from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, String, Boolean, Enum as SQLEnum, func


class Role(str, Enum):
    admin = "admin"
    normal = "normal"
    paid = "paid"
    owner = "owner"



class UserBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

    email: str = Field(
        sa_column=Column(String(255), nullable=False, unique=True, index=True)
    )

    username: Optional[str] = Field(
        default=None,
        sa_column=Column(String(50), unique=True, index=True, nullable=True)
    )


class User(UserBase, table=True):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    hashed_password: str = Field(
        sa_column=Column(String(255), nullable=False)
    )

    role: Role = Field(
        sa_column=Column(
            SQLEnum(Role, name="role"),
            default=Role.normal,
            nullable=False,
        )
    )

    email_verified: bool = Field(
        sa_column=Column(Boolean, default=False, nullable=False)
    )

    email_verified_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )

    two_factor_enabled: bool = Field(
        sa_column=Column(Boolean, default=False, nullable=False)
    )

    is_active: bool = Field(
        sa_column=Column(Boolean, default=True, nullable=False, index=True)
    )

    deleted_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True, index=True)
    )

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

    profile: Optional["Profile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False}
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email} role={self.role}>"