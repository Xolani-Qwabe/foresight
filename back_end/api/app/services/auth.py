from typing import Optional, Tuple
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlmodel import select
from app.models.db_models.user import Role

from app.utils.auth import AuthUtility
from app.models.db_models.user import User
from app.models.api_models.user import UserCreate, UserLogin, UserOutput


class AuthService:

    def __init__(self, auth_util: AuthUtility):
        self.auth_util = auth_util


    # Register
    def register(
        self,
        user_create: UserCreate,
        db: Session
    ) -> Tuple[UserOutput, str, str]:

        existing_user = db.exec(
            select(User).where(
                (User.email == user_create.email) |
                (User.username == user_create.username)
            )
        ).first()

        if existing_user:
            if existing_user.email == user_create.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )

        hashed_password = self.auth_util.hash_password(user_create.password)

        new_user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hashed_password,
            role=Role.normal,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        access_token = self.auth_util.create_access_token(
            {"sub": str(new_user.id)}
        )

        refresh_token = self.auth_util.create_refresh_token(
            {"sub": str(new_user.id)}
        )

        return (
            self._build_user_output(new_user),
            access_token,
            refresh_token
        )


    # Login
    def login(
        self,
        user_login: UserLogin,
        db: Session
    ) -> Tuple[UserOutput, str, str]:
        db_user: Optional[User] = db.exec(
            select(User).where((User.email == user_login.email) & (User.is_active == True))
        ).first()


        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not self.auth_util.verify_password(
            user_login.password,
            db_user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not db_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive account"
            )

        access_token = self.auth_util.create_access_token(
            {"sub": str(db_user.id)}
        )

        refresh_token = self.auth_util.create_refresh_token(
            {"sub": str(db_user.id)}
        )

        return (
            self._build_user_output(db_user),
            access_token,
            refresh_token
        )


    # Refresh Access Token
    def refresh_access_token(
        self,
        refresh_token: str,
        db: Session
    ) -> str:

        try:
            payload = self.auth_util.decode_token(
                refresh_token
              
            )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        db_user = db.exec(
            select(User).where(User.id == int(user_id))
        ).first()


        if not db_user or not db_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )

        return self.auth_util.create_access_token(
            {"sub": str(db_user.id)}
        )

 
    # Get Current User
    def get_current_user(
        self,
        token: str,
        db: Session
    ) -> UserOutput:

        try:
            payload = self.auth_util.decode_token(
                token
         
            )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        db_user = db.exec(
            select(User).where(User.id == int(user_id))
        ).first()


        if not db_user or not db_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user"
            )

        return self._build_user_output(db_user)


    # Mapper
    def _build_user_output(self, user: User) -> UserOutput:
        return UserOutput(
            id=user.id,
            email=user.email,
            username=user.username,
            role=user.role.value,
            email_verified=user.email_verified,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )