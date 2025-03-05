import pytest
from app.models.generated_text import GeneratedText
from app.repositories.generated_text_repository import GeneratedTextRepository


@pytest.fixture
def generated_text_repo(db_session):
    return GeneratedTextRepository(db_session)


def test_create_generated_text(generated_text_repo, user_factory, db_session):
    user = user_factory()
    text_entry = generated_text_repo.create_generated_text(user.id, "Hello AI", "AI Response")

    assert text_entry.id is not None
    assert text_entry.prompt == "Hello AI"
    assert text_entry.response == "AI Response"

    db_entry = db_session.get(GeneratedText, text_entry.id)
    assert db_entry is not None
    assert db_entry.user_id == user.id


def test_get_text_by_id(generated_text_repo, user_factory,  generated_text_factory):
    user = user_factory()
    text_entry = generated_text_factory(user_id=user.id)
    retrieved_text = generated_text_repo.get_generated_text_by_id(text_entry.id)

    assert retrieved_text is not None
    assert retrieved_text.id == text_entry.id


def test_get_all_texts_by_user(generated_text_repo, generated_text_factory, user_factory):
    user = user_factory()
    generated_text_factory(user_id=user.id)
    generated_text_factory(user_id=user.id)

    texts = generated_text_repo.get_all_texts_by_user(user.id)

    assert len(texts) == 2
    assert all(text.user_id == user.id for text in texts)


def test_delete_generated_text(generated_text_repo, user_factory, generated_text_factory, db_session):
    user = user_factory()
    text_entry = generated_text_factory(user_id=user.id)
    generated_text_repo.delete_generated_text(text_entry.id, user_id=user.id)

    db_entry = db_session.get(GeneratedText, text_entry.id)
    assert db_entry is None
