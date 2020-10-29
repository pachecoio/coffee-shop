import json
import pytest


def test_get_drinks_empty(app, client):
    res = client.get("/drinks")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert len(data["drinks"]) == 0


def test_get_drinks_details_fail_authorization(app, client):
    res = client.get("/drinks-detail")
    assert res.status_code == 401


def test_create_drink_fail_authorization(app, client):
    data = dict(
        title="Drink test", recipe=[{"name": "Coffee", "color": "black", "parts": 1}]
    )
    res = client.post("/drinks", data=data)
    assert res.status_code == 401


def test_update_drink_fail_authorization(app, client):
    data = dict(
        title="Drink test", recipe=[{"name": "Coffee", "color": "black", "parts": 1}]
    )
    res = client.patch("/drinks/1", data=data)
    assert res.status_code == 401


def test_delete_drink_fail_authorization(app, client):
    res = client.delete("/drinks/1")
    assert res.status_code == 401


def test_get_drinks_detail(app, client, barista_role):
    res = client.get("/drinks-detail", headers=barista_role)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert len(data["drinks"]) == 0


def test_create_drink_succeed_with_barista_role(app, client, barista_role):
    data = {
        "id": -1,
        "title": "Water3",
        "recipe": [{"name": "Water", "color": "blue", "parts": 1}],
    }
    res = client.post("/drinks", json=data, headers=barista_role)
    assert res.status_code == 201

    res = client.get("/drinks")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert len(data["drinks"]) == 1


def test_create_drink_succeed_with_manager_role(app, client, manager_role):
    data = {
        "id": -1,
        "title": "Water3",
        "recipe": [{"name": "Water", "color": "blue", "parts": 1}],
    }
    res = client.post("/drinks", json=data, headers=manager_role)
    assert res.status_code == 201

    res = client.get("/drinks")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert len(data["drinks"]) == 1


def test_update_drink_succeed_with_barista_role(app, client, barista_role):

    # Create a drink
    create_data = {
        "id": -1,
        "title": "Water3",
        "recipe": [{"name": "Water", "color": "blue", "parts": 1}],
    }
    res = client.post("/drinks", json=create_data, headers=barista_role)
    assert res.status_code == 201
    data = json.loads(res.data)

    update_dict = create_data.copy()
    update_dict["title"] = "Water4"

    # Test update item
    res = client.patch(
        "/drinks/{}".format(data["id"]), json=update_dict, headers=barista_role
    )
    assert res.status_code == 200


def test_update_drink_succeed_with_manager_role(app, client, manager_role):

    # Create a drink
    create_data = {
        "id": -1,
        "title": "Water3",
        "recipe": [{"name": "Water", "color": "blue", "parts": 1}],
    }
    res = client.post("/drinks", json=create_data, headers=manager_role)
    assert res.status_code == 201
    data = json.loads(res.data)

    update_dict = create_data.copy()
    update_dict["title"] = "Water4"

    # Test update item
    res = client.patch(
        "/drinks/{}".format(data["id"]), json=update_dict, headers=manager_role
    )
    assert res.status_code == 200


def test_delete_drink_fail_with_barista_role(app, client, barista_role):

    # Create a drink
    create_data = {
        "id": -1,
        "title": "Water3",
        "recipe": [{"name": "Water", "color": "blue", "parts": 1}],
    }
    res = client.post("/drinks", json=create_data, headers=barista_role)
    assert res.status_code == 201
    data = json.loads(res.data)

    # Test update item
    res = client.delete(
        "/drinks/{}".format(data["id"]), headers=barista_role
    )
    assert res.status_code == 401


def test_delete_drink_succeed_with_manager_role(app, client, manager_role):

    # Create a drink
    create_data = {
        "id": -1,
        "title": "Water3",
        "recipe": [{"name": "Water", "color": "blue", "parts": 1}],
    }
    res = client.post("/drinks", json=create_data, headers=manager_role)
    assert res.status_code == 201
    data = json.loads(res.data)

    # Test update item
    res = client.delete(
        "/drinks/{}".format(data["id"]), headers=manager_role
    )
    assert res.status_code == 200