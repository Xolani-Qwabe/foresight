from app.db.repository.user_auth_repository import UserRepository   
from app.db.schema.user import UserCreate, UserLogin, UserOutPut, UserWithToken
from app.core.security.auth_handler import AuthHandler
from app.core.security.hash_helper import HashHelper
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


class UserService:
    def __init__(self, db_session: Session):
        self.user_repository = UserRepository(session=db_session)
      
    
    def signup_user(self, user_data: UserCreate):
        if self.user_repository.user_exists(email=user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists. Please login instead."
            )

        hashed_password = HashHelper.hash_password(user_data.password)

        db_user_data = {
            "email": user_data.email,
            "hashed_password": hashed_password,
            "username": user_data.username or user_data.email.split("@")[0],
            "role": user_data.role,
        }

        return self.user_repository.create_user(db_user_data)

    
    def login_user(self, login_data: UserLogin) -> UserWithToken:
        print("Attempting to log in user:", login_data.username)
        user = self.user_repository.get_user_by_username(username=login_data.username)
        
        if not user or not HashHelper.verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )
        print("User authenticated successfully:", user.email)
        token = AuthHandler.sign_jwt(user_id = user.id)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Token generation failed."
            )
        return UserWithToken(
             user=UserOutPut.model_validate(user, from_attributes=True),
            token = token
        )
        
    def get_user_by_id(self, user_id: int):
        user = self.user_repository.get_user_by_id(user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )    
        return user