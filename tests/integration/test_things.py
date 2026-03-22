import pytest

NON_EXISTENT_ID = "00000000-0000-0000-0000-000000000000"


@pytest.mark.integration
async def test_create_thing(client):
    response = await client.post(
        "/things/",
        json={"name": "My Thing", "description": "A description"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My Thing"
    assert data["description"] == "A description"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.integration
async def test_create_thing_without_description(client):
    response = await client.post("/things/", json={"name": "Minimal Thing"})
    assert response.status_code == 201
    assert response.json()["description"] is None


@pytest.mark.integration
async def test_list_things(client):
    await client.post("/things/", json={"name": "Thing A"})
    await client.post("/things/", json={"name": "Thing B"})

    response = await client.get("/things/")
    assert response.status_code == 200
    assert len(response.json()) >= 2


@pytest.mark.integration
async def test_get_thing(client):
    create = await client.post("/things/", json={"name": "Fetchable Thing"})
    thing_id = create.json()["id"]

    response = await client.get(f"/things/{thing_id}")
    assert response.status_code == 200
    assert response.json()["id"] == thing_id


@pytest.mark.integration
async def test_get_thing_not_found(client):
    response = await client.get(f"/things/{NON_EXISTENT_ID}")
    assert response.status_code == 404


@pytest.mark.integration
async def test_update_thing(client):
    create = await client.post("/things/", json={"name": "Old Name"})
    thing_id = create.json()["id"]

    response = await client.put(f"/things/{thing_id}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


@pytest.mark.integration
async def test_update_thing_not_found(client):
    response = await client.put(f"/things/{NON_EXISTENT_ID}", json={"name": "Ghost"})
    assert response.status_code == 404


@pytest.mark.integration
async def test_delete_thing(client):
    create = await client.post("/things/", json={"name": "To Delete"})
    thing_id = create.json()["id"]

    response = await client.delete(f"/things/{thing_id}")
    assert response.status_code == 204

    response = await client.get(f"/things/{thing_id}")
    assert response.status_code == 404


@pytest.mark.integration
async def test_delete_thing_not_found(client):
    response = await client.delete(f"/things/{NON_EXISTENT_ID}")
    assert response.status_code == 404
