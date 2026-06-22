from fastapi.testclient import TestClient


def test_foodstuff_requires_valid_expiry_range(client: TestClient) -> None:
    response = client.post(
        "/foodstuffs",
        json={"name": "Milk", "category": "Dairy", "expiry_min_days": 7, "expiry_max_days": 3},
    )

    assert response.status_code == 422


def test_inventory_item_can_use_foodstuff_defaults_and_override_values(client: TestClient) -> None:
    foodstuff = client.post(
        "/foodstuffs",
        json={"name": "Milk", "category": "Dairy", "expiry_min_days": 3, "expiry_max_days": 7},
    ).json()

    created = client.post(
        "/inventory",
        json={
            "foodstuff_id": foodstuff["id"],
            "quantity_amount": "1.00",
            "quantity_unit": "carton",
            "purchase_date": "2026-06-22",
        },
    )

    assert created.status_code == 201
    item = created.json()
    assert item["name"] == "Milk"
    assert item["category"] == "Dairy"
    assert item["estimated_expiry_date"] == "2026-06-29"

    updated = client.patch(
        f"/inventory/{item['id']}",
        json={"name": "Lactose-free milk", "category": "Special dairy", "estimated_expiry_date": "2026-06-30"},
    ).json()

    assert updated["name"] == "Lactose-free milk"
    assert updated["category"] == "Special dairy"
    assert updated["estimated_expiry_date"] == "2026-06-30"


def test_inventory_lists_by_expiry_and_groups_by_category(client: TestClient) -> None:
    for payload in [
        {
            "name": "Yogurt",
            "category": "Dairy",
            "quantity_amount": "2.00",
            "quantity_unit": "cups",
            "purchase_date": "2026-06-22",
            "estimated_expiry_date": "2026-06-25",
        },
        {
            "name": "Carrot",
            "category": "Vegetables",
            "quantity_amount": "5.00",
            "quantity_unit": "pieces",
            "purchase_date": "2026-06-22",
            "estimated_expiry_date": "2026-07-01",
        },
    ]:
        assert client.post("/inventory", json=payload).status_code == 201

    items = client.get("/inventory").json()
    assert [item["name"] for item in items] == ["Yogurt", "Carrot"]

    groups = client.get("/inventory/grouped-by-category").json()
    assert [group["category"] for group in groups] == ["Dairy", "Vegetables"]


def test_remove_hides_active_inventory_without_eaten_or_wasted_semantics(client: TestClient) -> None:
    item = client.post(
        "/inventory",
        json={
            "name": "Apple",
            "category": "Fruit",
            "quantity_amount": "6.00",
            "quantity_unit": "pieces",
            "purchase_date": "2026-06-22",
            "estimated_expiry_date": "2026-06-28",
        },
    ).json()

    remove_response = client.delete(f"/inventory/{item['id']}")

    assert remove_response.status_code == 204
    assert client.get("/inventory").json() == []
    assert client.get(f"/inventory/{item['id']}").status_code == 405
