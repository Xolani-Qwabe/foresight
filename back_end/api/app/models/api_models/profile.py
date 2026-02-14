from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel
from .profile import SubscriptionTier

# profile create schema
class ProfileCreate(SQLModel):
    full_name: Optional[str] = None
    display_name: Optional[str] = None
    favorite_league: Optional[str] = None
    favorite_team: Optional[str] = None

# profile update schema
class ProfileUpdate(SQLModel):
    full_name: Optional[str] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    favorite_league: Optional[str] = None
    favorite_team: Optional[str] = None
    timezone: Optional[str] = None
    theme_preference: Optional[str] = None
    notification_enabled: Optional[bool] = None
