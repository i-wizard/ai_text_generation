import pytest
from unittest.mock import MagicMock
from werkzeug.security import generate_password_hash
from flask import Flask
from flask_jwt_extended import JWTManager
from app.services.auth_service import AuthService
from app.models.user import User


@pytest.fixture
def mock_user_repository():
    return MagicMock()

@pytest.fixture
def auth_service(mock_user_repository):
    return AuthService(mock_user_repository)

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "test_secret"
    JWTManager(app)
    return app


def test_register_user_success(auth_service, mock_user_repository):
    mock_user_repository.get_user_by_username.return_value = None
    mock_user_repository.create_user.return_value = User(id=1, username="testuser")

    user = auth_service.register_user("testuser", "securepassword")

    assert user.id == 1
    assert user.username == "testuser"
    mock_user_repository.create_user.assert_called_once()


def test_register_user_already_exists(auth_service, mock_user_repository):
    mock_user_repository.get_user_by_username.return_value = User(username="testuser")

    with pytest.raises(Exception) as exc_info:
        auth_service.register_user("testuser", "securepassword")

    assert exc_info.value.code == 409


def test_login_user_success(auth_service, mock_user_repository, app):
    hashed_password = generate_password_hash("securepassword")
    mock_user_repository.get_user_by_username.return_value = User(id=1, username="testuser", password_hash=hashed_password)

    with app.app_context():
        user, access_token = auth_service.login_user("testuser", "securepassword")

    assert user.id == 1
    assert access_token is not None


def test_login_invalid_credentials(auth_service, mock_user_repository):
    mock_user_repository.get_user_by_username.return_value = None

    with pytest.raises(Exception) as exc_info:
        auth_service.login_user("testuser", "wrongpassword")

    assert exc_info.value.code == 401
