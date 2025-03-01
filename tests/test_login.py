import pytest


@pytest.mark.parametrize(
    "payload, expected_error",
    [
        ({"username": "testuser", "password": "wrongpassword"}, "Invalid credentials"),
        (
            {"username": "wronguser", "password": "securepassword"},
            "Invalid credentials",
        ),
    ],
)
def test_login_wrong_credentials(client, payload, expected_error):
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401

    data = response.get_json()


def test_login_success(client, db_session, user_factory):
    test_user = user_factory(username="testuser", password="securepassword")
    db_session.add(test_user)
    db_session.commit()

    payload = {"username": "testuser", "password": "securepassword"}
    response = client.post("/api/v1/auth/login", json=payload)

    assert response.status_code == 200

    data = response.get_json()["data"]
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert "username" in data
    assert "id" in data
    assert data["username"] == payload["username"]
    assert "password" not in data
