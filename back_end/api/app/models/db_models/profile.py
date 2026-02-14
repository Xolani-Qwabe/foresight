from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func



# Subscription Tier Enum
class SubscriptionTier(str, Enum):
    free = "free"
    pro = "pro"
    premium = "premium"

class SubscriptionStatus(str, Enum):
    active = "active"
    expired = "expired"
    canceled = "canceled"
    trial = "trial"

# Database Model
class Profile(SQLModel, table=True):
    __tablename__ = "user_profiles"

    profile_id: Optional[int] = Field(default=None, primary_key=True)
    # Identity / Public Info
    full_name: Optional[str] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    # Preferences
    favorite_league: Optional[str] = None
    favorite_team: Optional[str] = None
    timezone: str = Field(default="UTC")
    notification_enabled: bool = Field(default=True)
    theme_preference: Optional[str] = Field(default="light")
    # Subscription
    subscription_tier: SubscriptionTier = Field(
        default=SubscriptionTier.free
    )
    subscription_status: SubscriptionStatus = Field(
        default=SubscriptionStatus.active
    )
    subscription_started_at: Optional[datetime] = None
    subscription_expires_at: Optional[datetime] = None
    # Usage / Analytics
    last_login_at: Optional[datetime] = None
    last_active_at: Optional[datetime] = None
    login_count: int = Field(default=0)
    prediction_count: int = Field(default=0)
    # Audit timestamps (DB controlled)
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
    # One-to-one ownership
    user_id: int = Field(
        foreign_key="users.id",
        unique=True,
        nullable=False,
        index=True,
    )
    user: Optional["User"] = Relationship(
        back_populates="profile"
    )
