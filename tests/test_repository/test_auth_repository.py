import pytest
from app.models.user import User
from app.repositories.user_repository import UserRepository
from werkzeug.security import generate_password_hash


@pytest.fixture
def user_repo(db_session):
    return UserRepository(db_session)


def test_create_user(user_repo, db_session):
    user = user_repo.create_user("testuser", generate_password_hash("strongpassword1"))

    assert user.id is not None
    assert user.username == "testuser"

    db_user = db_session.get(User, user.id)
    assert db_user is not None
    assert db_user.username == "testuser"


def test_get_user_by_username(user_repo, user_factory):
    user = user_factory(username="existinguser", password=generate_password_hash("password123"))
    retrieved_user = user_repo.get_user_by_username("existinguser")

    assert retrieved_user is not None
    assert retrieved_user.username == "existinguser"


def test_get_user_by_id(user_repo, user_factory):
    user = user_factory(username="user1", password=generate_password_hash("secretepassword3"))
    retrieved_user = user_repo.get_user_by_id(user.id)

    assert retrieved_user is not None
    assert retrieved_user.id == user.id


def test_delete_user(user_repo, user_factory, db_session):
    user = user_factory(username="user2", password=generate_password_hash("secretepassword2"))
    user_repo.delete_user(user)

    db_user = db_session.get(User, user.id)
    assert db_user is None
