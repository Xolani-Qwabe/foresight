from sqlalchemy.orm import Session

class BaseAuthRepository:
    def __init__(self, session : Session):
        self.session = session