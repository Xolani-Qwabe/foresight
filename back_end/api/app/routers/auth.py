from fastapi import APIRouter, Depends
from app.db.schema.user import UserCreate, UserLogin, UserOutPut, UserWithToken
from app.core.database_connection import get_db_session
from sqlalchemy.orm import Session
from app.service.user_service import UserService

auth_router = APIRouter()

@auth_router.post("/login", status_code=200, response_model=UserWithToken)
async def login(login_data: UserLogin, db_session: Session = Depends(get_db_session)):
    try:
        return UserService(db_session=db_session).login_user(login_data=login_data)
    except Exception as error:
        print("Error during login:", str(error))
        raise error

@auth_router.post("/signup", status_code=201, response_model=UserOutPut)
async def signup(user_data: UserCreate, db_session: Session = Depends(get_db_session)):
   try:
       return UserService(db_session=db_session).signup_user(user_data=user_data)
   except Exception as error:
       print("Error during signup:", str(error))
       raise error

'''
router -> service -> repository -> db
router <- service <- repository <- db
'''
