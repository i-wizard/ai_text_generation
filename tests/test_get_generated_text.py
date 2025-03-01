import pytest
from flask_jwt_extended import create_access_token


@pytest.fixture
def auth_header(db_session, user_factory):
    test_user = user_factory(username="testuser", password="securepassword")
    token = create_access_token(identity=test_user.id)
    return {"Authorization": f"Bearer {token}", "user_id": test_user.id}


@pytest.fixture
def user_2_auth_header(db_session, user_factory):
    another_user = user_factory(username="anotheruser", password="securepassword")
    token = create_access_token(identity=another_user.id)
    return {"Authorization": f"Bearer {token}", "user_id": another_user.id}


@pytest.fixture
def generated_text_entry(db_session, generated_text_factory, auth_header):
    return generated_text_factory(
        user_id=auth_header["user_id"], prompt="Hello AI", response="AI Response"
    )


def test_get_generated_text_by_id(client, auth_header, generated_text_entry):
    response = client.get(
        f"/api/v1/text-generations/{generated_text_entry.id}", headers=auth_header
    )

    assert response.status_code == 200
    data = response.get_json()["data"]

    assert data["id"] == generated_text_entry.id
    assert data["prompt"] == "Hello AI"
    assert data["response"] == "AI Response"
    assert data["user_id"] == auth_header["user_id"]


def test_cannot_access_another_users_generated_text(
    client, user_2_auth_header, generated_text_entry
):

    response = client.get(
        f"/api/v1/text-generations/{generated_text_entry.id}",
        headers=user_2_auth_header,
    )

    assert response.status_code == 404
