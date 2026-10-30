from conftest import login, register


def class_data(name="Yoga Pagi", instructor="Rina", start_time="08:00:00", level="beginner"):
    return {
        "class_name": name,
        "instructor": instructor,
        "date": "2026-11-10",
        "start_time": start_time,
        "duration_min": 60,
        "capacity": 12,
        "level": level,
    }


def create_class(client, headers, **changes):
    response = client.post("/classes", headers=headers, json={**class_data(), **changes})
    assert response.status_code == 201, response.text
    return response.json()


def test_guest_can_read_but_cannot_create_class(client):
    assert client.post("/classes", json=class_data()).status_code == 401
    register(client)
    created = create_class(client, login(client))
    assert created["class_name"] == "Yoga Pagi"
    assert created["instructor"] == "Rina"
    assert created["level"] == "beginner"
    assert client.get(f"/classes/{created['id']}").status_code == 200
    assert client.get("/classes").json()["total"] == 1


def test_user_can_update_own_class_but_not_another_users_class(client):
    first = register(client, "User A", "usera@example.com")
    a_headers = login(client, "usera@example.com")
    item = create_class(client, a_headers)
    assert item["owner_id"] == first["id"]

    register(client, "User B", "userb@example.com")
    b_headers = login(client, "userb@example.com")
    assert client.patch(f"/classes/{item['id']}", headers=b_headers, json={"capacity": 20}).status_code == 403
    assert client.delete(f"/classes/{item['id']}", headers=b_headers).status_code == 403

    own = client.patch(f"/classes/{item['id']}", headers=a_headers, json={"class_name": "Yoga Sore", "capacity": 18})
    assert own.status_code == 200
    assert own.json()["class_name"] == "Yoga Sore"
    assert own.json()["capacity"] == 18


def test_admin_can_manage_any_class(client):
    register(client)
    item = create_class(client, login(client))
    admin_headers = login(client, "admin@example.com")
    assert client.patch(f"/classes/{item['id']}", headers=admin_headers, json={"level": "advanced"}).status_code == 200
    assert client.delete(f"/classes/{item['id']}", headers=admin_headers).status_code == 204
    assert client.get(f"/classes/{item['id']}").status_code == 404


def test_instructor_cannot_have_two_classes_at_same_time(client):
    register(client)
    headers = login(client)
    create_class(client, headers)
    response = client.post("/classes", headers=headers, json=class_data(name="Pilates"))
    assert response.status_code == 409
    another = create_class(client, headers, instructor="Budi", class_name="Pilates")
    assert another["class_name"] == "Pilates"


def test_search_pagination_and_validation(client):
    register(client)
    headers = login(client)
    create_class(client, headers)
    create_class(client, headers, class_name="HIIT", instructor="Budi", start_time="09:00:00", level="advanced")
    result = client.get("/classes?search=yoga&skip=0&limit=1")
    assert result.status_code == 200
    assert result.json()["total"] == 1
    assert result.json()["items"][0]["class_name"] == "Yoga Pagi"
    assert client.post("/classes", headers=headers, json={**class_data(), "capacity": 0}).status_code == 422
