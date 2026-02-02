from app.core.database_connection import Base, engine
from app.db.models import user
 
 
def create_tables():
    Base.metadata.create_all(bind=engine)