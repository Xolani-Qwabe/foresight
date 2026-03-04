from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session

from app.services.auth import AuthService
from app.utils.auth import AuthUtility
from app.utils.db import DBUtility
from app.models.api_models.user import UserCreate, UserLogin, UserOutput

import os
from dotenv import load_dotenv

router = APIRouter(prefix="/api/auth", tags=["auth"])

load_dotenv()
POSTGRES_CONNECTION_STRING = os.getenv("POSTGRES_CONNECTION_STRING")

# Auth Utilities
auth_util = AuthUtility()
auth_service = AuthService(auth_util)

# Database Utility (sync)
db_util = DBUtility(
    POSTGRES_CONNECTION_STRING,
    echo=True
)


# Cookie Dependency
def get_current_user(
    request: Request,
    db: Session = Depends(db_util.get_db_dependency())
) -> UserOutput:

    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return auth_service.get_current_user(token, db)  # sync now



# Register
@router.post("/register", response_model=UserOutput)
def register(
    user: UserCreate,
    response: Response,
    db: Session = Depends(db_util.get_db_dependency())
):
    user_output, access_token, refresh_token = auth_service.register(user, db)

    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=900
    )

    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=604800
    )

    return user_output



# Login
@router.post("/login", response_model=UserOutput)
def login(
    user: UserLogin,
    response: Response,
    db: Session = Depends(db_util.get_db_dependency())
):
    user_output, access_token, refresh_token = auth_service.login(user, db)

    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=900
    )

    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=604800
    )

    return user_output



# Refresh Endpoint
@router.post("/refresh")
def refresh_token(
    request: Request,
    response: Response,
    db: Session = Depends(db_util.get_db_dependency())
):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    new_access_token = auth_service.refresh_access_token(refresh_token, db)

    response.set_cookie(
        "access_token",
        new_access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=900
    )

    return {"message": "Access token refreshed"}


# Logout
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}



# Me
@router.get("/session", response_model=UserOutput)
def me(current_user: UserOutput = Depends(get_current_user)):
    return current_user