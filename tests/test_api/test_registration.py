import pytest


def test_register_success(client):
    payload = {"username": "testuser", "password": "securepassword"}
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User registered successfully"
    assert "data" in data
    assert "id" in data["data"]
    assert data["data"]["username"] == payload["username"]


def test_register_duplicate_username(client):
    payload = {"username": "testuser", "password": "securepassword"}
    client.post("/api/v1/auth/register", json=payload)

    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 409


@pytest.mark.parametrize(
    "payload, expected_error_field",
    [
        ({"username": "", "password": "securepassword"}, "username"),
        ({"username": "testuser", "password": ""}, "password"),
        ({"username": "", "password": ""}, "username"),
    ],
)
def test_register_invalid_input(client, payload, expected_error_field):
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 422
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid input"
    assert data["details"][0]["loc"][0] == expected_error_field


@pytest.mark.parametrize(
    "payload, expected_error_field, expected_error_message",
    [
        (
            {"username": "it", "password": "securepassword"},
            "username",
            "String should have at least 3 characters",
        ),
        (
            {"username": "testuser", "password": "short"},
            "password",
            "String should have at least 6 characters",
        ),
    ],
)
def test_short_password_or_username(
    client, payload, expected_error_field, expected_error_message
):
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 422
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid input"
    assert data["details"][0]["loc"][0] == expected_error_field
    assert data["details"][0]["msg"] == expected_error_message
