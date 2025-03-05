from unittest.mock import patch

import pytest
from flask_jwt_extended import create_access_token


@pytest.fixture
def auth_header(db_session, user_factory):
    test_user = user_factory(username="testuser", password="securepassword")
    token = create_access_token(identity=test_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_openai():
    with patch("app.clients.openai.OpenAIProvider.generate_text") as mock:
        mock.return_value = "This is a mocked AI-generated response."
        yield mock


def test_generate_text_success(client, auth_header, mock_openai):
    payload = {"prompt": "Write a short poem about AI"}
    response = client.post(
        "/api/v1/text-generations/", json=payload, headers=auth_header
    )

    assert response.status_code == 201
    data = response.get_json()["data"]
    assert "id" in data
    assert "response" in data
    assert "prompt" in data
    assert "timestamp" in data
    assert "user_id" in data
    assert data["prompt"] == payload["prompt"]
    assert mock_openai.return_value == data["response"]
    mock_openai.assert_called_once_with(payload["prompt"])


def test_generate_text_unauthorized(client):
    payload = {"prompt": "Write a short story about space"}
    response = client.post("/api/v1/text-generations/", json=payload)

    assert response.status_code == 401
    assert "msg" in response.get_json()


def test_generate_text_validation_without_prompt_failure(client, auth_header):
    response = client.post("/api/v1/text-generations/", json={}, headers=auth_header)

    assert response.status_code == 422
    data = response.get_json()

    assert "error" in data
    assert data["error"] == "Invalid input"
    assert data["details"][0]["loc"][0] == "prompt"


def test_generate_text_validation_with_short_prompt_failure(client, auth_header):
    response = client.post(
        "/api/v1/text-generations/", json={"prompt": "two"}, headers=auth_header
    )

    assert response.status_code == 422
    data = response.get_json()

    assert "error" in data
    assert data["error"] == "Invalid input"
    assert data["details"][0]["loc"][0] == "prompt"
    assert data["details"][0]["msg"] == "String should have at least 5 characters"
