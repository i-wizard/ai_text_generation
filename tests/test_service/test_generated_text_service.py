import pytest
from unittest.mock import MagicMock, patch
from flask import Flask
from flask import abort
from app.services.generated_text_service import GeneratedTextService
from app.models.generated_text import GeneratedText
from app.models.user import User


@pytest.fixture
def mock_generated_text_repository():
    return MagicMock()


@pytest.fixture
def mock_user_repository():
    return MagicMock()


@pytest.fixture
def generated_text_service(mock_generated_text_repository, mock_user_repository):
    return GeneratedTextService(mock_generated_text_repository, mock_user_repository)


@pytest.fixture
def app():
    """Flask app context for handling abort()"""
    app = Flask(__name__)
    return app


def test_create_text_success(generated_text_service, mock_user_repository, mock_generated_text_repository):

    mock_user_repository.get_user_by_id.return_value = User(id=1, username="testuser")
    mock_ai_provider = MagicMock()
    mock_ai_provider.generate_text.return_value = "Generated AI response"

    mock_generated_text_repository.create_generated_text.return_value = GeneratedText(
        id=1, user_id=1, prompt="Hello AI", response="Generated AI response"
    )

    with patch("app.services.generated_text_service.AITextGeneratorProviderFactory.get_provider",
               return_value=mock_ai_provider):
        generated_text = generated_text_service.create_text(1, "Hello AI")

    assert generated_text.user_id == 1
    assert generated_text.response == "Generated AI response"
    mock_generated_text_repository.create_generated_text.assert_called_once()


def test_create_text_user_not_found(generated_text_service, mock_user_repository, app):
    mock_user_repository.get_user_by_id.return_value = None

    with app.app_context(), pytest.raises(Exception) as exc_info:
        generated_text_service.create_text(1, "Hello AI")

    assert exc_info.value.code == 404


def test_get_text_success(generated_text_service, mock_generated_text_repository):

    mock_generated_text_repository.get_generated_text_by_id_and_user.return_value = (
        GeneratedText(
            id=1, user_id=1, prompt="Test prompt", response="Generated response"
        )
    )

    text = generated_text_service.get_text(1, 1)

    assert text.id == 1
    assert text.response == "Generated response"


def test_get_text_not_found(
    generated_text_service, mock_generated_text_repository, app
):

    mock_generated_text_repository.get_generated_text_by_id_and_user.return_value = None

    with app.app_context(), pytest.raises(Exception) as exc_info:
        generated_text_service.get_text(1, 1)

    assert exc_info.value.code == 404



def test_update_text_success(generated_text_service, mock_generated_text_repository):

    mock_generated_text_repository.get_generated_text_by_id_and_user.return_value = GeneratedText(
        id=1, user_id=1, prompt="Test prompt", response="Old response"
    )
    mock_ai_provider = MagicMock()
    mock_ai_provider.generate_text.return_value = "Updated AI response"

    mock_generated_text_repository.update_generated_text.return_value = GeneratedText(
        id=1, user_id=1, prompt="Test prompt", response="Updated AI response"
    )

    with patch("app.services.generated_text_service.AITextGeneratorProviderFactory.get_provider", return_value=mock_ai_provider):
        updated_text = generated_text_service.update_text(1, 1)

    assert updated_text.response == "Updated AI response"
    mock_generated_text_repository.update_generated_text.assert_called_once()


def test_update_text_not_found(
    generated_text_service, mock_generated_text_repository, app
):
    mock_generated_text_repository.get_generated_text_by_id_and_user.return_value = None

    with app.app_context(), pytest.raises(Exception) as exc_info:
        generated_text_service.update_text(1, 1)

    assert exc_info.value.code == 404


def test_delete_text_success(generated_text_service, mock_generated_text_repository):
    mock_generated_text_repository.delete_generated_text.return_value = True

    response = generated_text_service.delete_text(1, 1)

    assert response is None
    assert mock_generated_text_repository.delete_generated_text.called


def test_delete_text_not_found(
    generated_text_service, mock_generated_text_repository, app
):

    mock_generated_text_repository.delete_generated_text.return_value = False

    with app.app_context(), pytest.raises(Exception) as exc_info:
        generated_text_service.delete_text(1, 1)

    assert exc_info.value.code == 404
