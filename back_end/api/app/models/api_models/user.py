from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel
from .profile import SubscriptionTier

# registration schema
class UserCreate(SQLModel):
    email: str
    password: str
    username: Optional[str] = None

# login schema
class UserLogin(SQLModel):
    username: str
    password: str

# public user schema
class UserOutput(SQLModel):
    id: int
    email: str
    username: Optional[str]
    role: str
    email_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
