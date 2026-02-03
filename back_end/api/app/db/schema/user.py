from pydantic import BaseModel, EmailStr
from typing import Union
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    normal = "user"
    paid = "paid_user"
    owner = "owner"
    
class UserCreate(BaseModel):
    email : EmailStr
    password  : str
    username : Union[str, None] = None
    role : str
    
class UserOutPut(BaseModel):
    id: int
    email: EmailStr
    username: str | None
    role: str 
    
class UserUpdate(BaseModel):
    id : int
    email : Union[EmailStr, None] = None
    role : Union[str, None] = None
    password : Union[str, None] = None
      
class UserLogin(BaseModel):
    username : str
    password : str
    
class UserWithToken(BaseModel):
    user : UserOutPut
    token : str
    
