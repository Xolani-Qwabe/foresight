from fastapi import FastAPI, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth import auth as auth_router


from app.utils.db import DBUtility
from dotenv import load_dotenv
import os

from contextlib import asynccontextmanager

load_dotenv()
POSTGRES_CONNECTION_STRING = os.getenv("POSTGRES_CONNECTION_STRING")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    # Initialize db at start
    print("Creating tables...")
    DBUtility(engine_url=POSTGRES_CONNECTION_STRING, echo=True, async_mode=False).create_tables()
    yield
    # Shutdown code


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)



@app.get("/health")
async def health_check():
    return {"status": "Application is running"}

@app.get("/")
async def root():
    return {"message": "Welcome To Foresight"}

