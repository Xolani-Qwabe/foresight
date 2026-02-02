from fastapi import FastAPI, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.utils.init_db import create_tables
from app.routers.auth import auth_router


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

