from conftest import login, register


def test_admin_creates_user_and_user_can_login(client):
    user = register(client, "User A", " USERA@example.com ")
    assert user["role"] == "user"
    assert "password_hash" not in user

    headers = login(client, "usera@example.com")
    current = client.get("/auth/me", headers=headers)
    assert current.status_code == 200
    assert current.json()["email"] == "usera@example.com"
    assert "password_hash" not in current.json()


def test_only_admin_creates_accounts_and_role_cannot_be_chosen(client):
    data = {"name": "User B", "email": "userb@example.com", "password": "password123", "role": "admin"}
    assert client.post("/auth/register", json=data).status_code == 401

    register(client, "User A", "usera@example.com")
    assert client.post("/auth/register", json=data, headers=login(client, "usera@example.com")).status_code == 403

    created = client.post("/auth/register", json=data, headers=login(client, "admin@example.com"))
    assert created.status_code == 201
    assert created.json()["role"] == "user"
    assert "password_hash" not in created.json()


def test_user_a_updates_own_profile_but_user_b_cannot(client):
    user_a = register(client, "User A", "usera@example.com")
    register(client, "User B", "userb@example.com")
    a_headers = login(client, "usera@example.com")
    b_headers = login(client, "userb@example.com")

    own = client.patch(f"/users/{user_a['id']}", json={"name": "User A Updated"}, headers=a_headers)
    assert own.status_code == 200
    assert own.json()["name"] == "User A Updated"
    assert "password_hash" not in own.json()

    denied = client.patch(f"/users/{user_a['id']}", json={"name": "Changed by B"}, headers=b_headers)
    assert denied.status_code == 403
    assert client.get(f"/users/{user_a['id']}", headers=b_headers).status_code == 403
    assert client.get(f"/users/{user_a['id']}", headers=a_headers).json()["name"] == "User A Updated"


def test_admin_can_update_other_user_and_duplicate_email_conflicts(client):
    user_a = register(client, "User A", "usera@example.com")
    register(client, "User B", "userb@example.com")
    admin = login(client, "admin@example.com")
    updated = client.patch(f"/users/{user_a['id']}", json={"name": "Admin Edited"}, headers=admin)
    assert updated.status_code == 200
    assert updated.json()["name"] == "Admin Edited"
    duplicate = client.patch(f"/users/{user_a['id']}", json={"email": "userb@example.com"}, headers=admin)
    assert duplicate.status_code == 409


def test_invalid_login_is_unauthorized(client):
    register(client)
    response = client.post("/auth/login", json={"email": "trainer@example.com", "password": "wrong-password"})
    assert response.status_code == 401


def test_auth_me_requires_valid_token(client):
    assert client.get("/auth/me").status_code == 401
    assert client.get("/auth/me", headers={"Authorization": "Bearer invalid"}).status_code == 401
