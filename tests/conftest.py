import pytest
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.config import TestConfig
from app.models.user import User


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db.session


@pytest.fixture
def user_factory(db_session):
    def create_user(username, password):
        hashed_password = generate_password_hash(password)
        user = User(username=username, password_hash=hashed_password)
        db_session.add(user)
        db_session.commit()
        return user

    return create_user


from app.models.generated_text import GeneratedText


@pytest.fixture
def generated_text_factory(db_session):
    def _create_generated_text(
        user_id, prompt="Default prompt", response="Generated response"
    ):
        generated_text = GeneratedText(
            user_id=user_id, prompt=prompt, response=response
        )
        db_session.add(generated_text)
        db_session.commit()
        return generated_text

    return _create_generated_text
