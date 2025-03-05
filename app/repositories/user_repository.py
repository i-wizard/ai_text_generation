from typing import Optional

from app.models.user import User
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_user(self, username: str, password_hash: str) -> User:
        new_user = User(username=username, password_hash=password_hash)
        self.db_session.add(new_user)
        self.db_session.commit()
        return new_user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db_session.query(User).filter_by(id=user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db_session.query(User).filter_by(username=username).first()

    def delete_user(self, user: User) -> None:
        self.db_session.delete(user)
        self.db_session.commit()