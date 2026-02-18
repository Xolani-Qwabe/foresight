from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

from app.services.auth import AuthService
from app.utils.auth import AuthUtility
from app.utils.db import DBUtility
from app.models.api_models.user import UserCreate, UserLogin, UserWithToken, UserOutput
from app.models.db_models.user import User
from sqlmodel import select

from dotenv import load_dotenv
import os

# Initialize
router = APIRouter(prefix="/auth", tags=["auth"])

auth_util = AuthUtility()
auth_service = AuthService(auth_util)

load_dotenv()
POSTGRES_CONNECTION_STRING = os.getenv("POSTGRES_CONNECTION_STRING")

db_util = DBUtility(POSTGRES_CONNECTION_STRING, echo=True, async_mode=False)

# OAuth2 scheme for Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# get current user 
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(db_util.get_db_dependency())) -> UserOutput:
    return await auth_service.get_current_user(token, db)


# Registration route
@router.post("/register", response_model=UserWithToken)
async def register(user: UserCreate, db: AsyncSession = Depends(db_util.get_db_dependency())):
    """
    Register a new user and return access + refresh tokens with user info
    """
    return await auth_service.register(user, db)

# Login route
@router.post("/login", response_model=UserWithToken)
async def login(user: UserLogin, db: AsyncSession = Depends(db_util.get_db_dependency())):
    """
    Login user and return access + refresh tokens with user info
    """
    return await auth_service.login(user, db)


@router.get("/me", response_model=UserOutput)
async def me(current_user: UserOutput = Depends(get_current_user)):
    """
    Get the currently authenticated user
    """
    return current_user
