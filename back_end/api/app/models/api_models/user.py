from datetime import datetime
from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field
from pydantic import EmailStr


# Role Enum
class Role(str, Enum):
    admin = "admin"
    normal = "normal"
    paid = "paid"
    owner = "owner"


# Registration Schema
class UserCreate(SQLModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    username: Optional[str] = Field(default=None, min_length=3, max_length=30)


# Login Schema
class UserLogin(SQLModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


# Public User Schema
class UserOutput(SQLModel):
    id: int
    email: EmailStr
    username: Optional[str]
    role: Role  # Use the Enum here instead of str
    email_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }