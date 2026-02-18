from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class AuthUtility:
    """
    Utility class for low-level auth operations: hashing, JWT generation & verification.
    """

    def __init__(
        self,
        secret_key: str = os.getenv("JWT_SECRETE"),
        algorithm: str = os.getenv("JWT_ALGORITHM", "HS256"),
        access_exp_minutes: int = 15,
        refresh_exp_days: int = 7,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_exp_minutes = access_exp_minutes
        self.refresh_exp_days = refresh_exp_days
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Password hashing & verification
    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    # JWT Token generation & verification
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=self.access_exp_minutes))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=self.refresh_exp_days))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
