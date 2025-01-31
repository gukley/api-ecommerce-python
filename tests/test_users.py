def test_create_user(client, setup_db):
    response = client.post(
        "/register",
        json={"name": "John Doe", "email": "john@example.com", "password": "123456"},
    )
    assert response.status_code == 201
    assert response.json()["email"] == "john@example.com"


def test_get_user_authenticated(client, setup_db):
    register_response = client.post(
        "/register",
        json={"name": "John Doe", "email": "john@example.com", "password": "123456"},
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/login",
        json={"email": "john@example.com", "password": "123456"},
    )
    assert login_response.status_code == 200
    token = login_response.json().get("token")
    assert token is not None

    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["email"] == "john@example.com"
