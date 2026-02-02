from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv


load_dotenv()

URL = os.getenv("DATABASE_URL")

engine = create_engine(URL)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db_session():
    db = local_session()
    try:
        yield db
    finally:
        db.close()
        
