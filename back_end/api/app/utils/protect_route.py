
from fastapi import Depends, HTTPException, Header, status
from typing import Annotated
from sqlalchemy.orm import Session
from app.core.security.auth_handler import AuthHandler
from app.service.user_service import UserService
from app.core.database_connection import get_db_session
from app.db.schema.user import UserOutPut


AUTH_PREFIX = 'Bearer'


def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    db_session: Session = Depends(get_db_session)
) -> UserOutPut:
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not authorization:
        raise auth_exception

    if not authorization.startswith("Bearer "):
        raise auth_exception

    token = authorization.removeprefix("Bearer ").strip()
    payload = AuthHandler.decode_jwt(token)

    user_id = payload.get("user_id") if payload else None
    if not user_id:
        raise auth_exception

    user_service = UserService(db_session=db_session)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise auth_exception

    return UserOutPut.model_validate(user, from_attributes=True)

    