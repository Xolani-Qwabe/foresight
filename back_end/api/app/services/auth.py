from typing import Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.utils.auth import AuthUtility
from app.models.db_models.user import User
from app.models.api_models.user import UserCreate, UserLogin, UserOutput, UserWithToken


class AuthService:
    """
    AuthService contains authentication business logic using SQLModel.
    Returns UserWithToken objects for login/register.
    """

    def __init__(self, auth_util: AuthUtility):
        self.auth_util = auth_util

    # --- Registration ---
    async def register(self, user_create: UserCreate, db: AsyncSession) -> UserWithToken:
  
        query = select(User).where(User.email == user_create.email)
        result = db.execute(query)
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

    
        hashed_password = self.auth_util.hash_password(user_create.password)

   
        new_user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    
        access_token = self.auth_util.create_access_token({"sub": new_user.username})
        refresh_token = self.auth_util.create_refresh_token({"sub": new_user.username})

        return UserWithToken(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserOutput(
                id=new_user.id,
                email=new_user.email,
                username=new_user.username,
                role=new_user.role.value,
                email_verified=new_user.email_verified,
                is_active=new_user.is_active,
                created_at=new_user.created_at,
                updated_at=new_user.updated_at
            )
        )

    # --- Login ---
    async def login(self, user_login: UserLogin, db: AsyncSession) -> UserWithToken:
        
        query = select(User).where(User.username == user_login.username)
        result = await db.execute(query)
        db_user: Optional[User] = result.scalar_one_or_none()

        if not db_user or not self.auth_util.verify_password(user_login.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

      
        access_token = self.auth_util.create_access_token({"sub": db_user.username})
        refresh_token = self.auth_util.create_refresh_token({"sub": db_user.username})

        return UserWithToken(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserOutput(
                id=db_user.id,
                email=db_user.email,
                username=db_user.username,
                role=db_user.role.value,
                email_verified=db_user.email_verified,
                is_active=db_user.is_active,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at
            )
        )

    # Get current user from token (used in protected routes)
    async def get_current_user(self, token: str, db: AsyncSession) -> UserOutput:
        try:
            payload = self.auth_util.decode_token(token)
            username = payload.get("sub")
            if not username:
                raise HTTPException(status_code=401, detail="Invalid token")
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))

        query = select(User).where(User.username == username)
        result = await db.execute(query)
        db_user: Optional[User] = result.scalar_one_or_none()
        if not db_user or not db_user.is_active:
            raise HTTPException(status_code=401, detail="Inactive user")

        return UserOutput(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            role=db_user.role.value,
            email_verified=db_user.email_verified,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
