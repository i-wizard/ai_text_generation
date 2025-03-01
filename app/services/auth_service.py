from flask import abort
from flask_jwt_extended import create_access_token
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash

from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, username: str, password: str):
        if self.user_repository.get_user_by_username(username):
            abort(409, description="Username already taken")

        hashed_password = generate_password_hash(password)
        user = self.user_repository.create_user(username, hashed_password)

        return user

    def login_user(self, username: str, password: str):
        user = self.user_repository.get_user_by_username(username)
        if not user or not check_password_hash(user.password_hash, password):
            abort(401, description="Invalid credentials")

        access_token = create_access_token(
            identity=user.id, expires_delta=timedelta(hours=1)
        )
        return user, access_token
