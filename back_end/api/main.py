from fastapi import FastAPI, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.utils.protect_route import get_current_user
from app.utils.init_db import create_tables
from app.routers.auth import auth_router
from app.db.schema.user import UserOutPut

from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    # Initialize db at start
    print("Creating tables...")
    create_tables()
    yield
    # Shutdown code


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(router=auth_router, tags=["Authentication"])

@app.get("/health")
async def health_check():
    return {"status": "Application is running"}

@app.get("/")
async def root():
    return {"message": "Welcome To Foresight"}

@app.get("/protected-route")
async def read_protected_route(current_user: UserOutPut = Depends(get_current_user)):
    return {"status": "Application is running", "user": current_user.username }


