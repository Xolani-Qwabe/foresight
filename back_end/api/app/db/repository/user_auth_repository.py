from .base_auth import BaseAuthRepository
from app.db.models.user import User


class UserRepository(BaseAuthRepository):
    
    def create_user(self, user_data: dict) -> User:
        new_user = User(**user_data)

        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user


    def user_exists(self, email: str) -> bool:
        user = self.session.query(User).filter_by(email=email).first() 
        return bool(user)

    def get_user_by_email(self, email: str) -> User | None:
        user = self.session.query(User).filter_by(email=email).first() 
        return user
    def get_user_by_username(self, username: str) -> User | None:
        user = self.session.query(User).filter_by(username=username).first() 
        return user
    
    def get_user_by_id(self, user_id: int) ->User | None:
        user = self.session.query(User).filter_by(id=user_id).first() 
        return user