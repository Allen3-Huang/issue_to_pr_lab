from fastapi.testclient import TestClient


def test_list_products(client: TestClient) -> None:
    response = client.get("/products")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 6
    assert body["page"] == 1
    assert body["page_size"] == 20
    assert body["total_pages"] == 1
    assert body["items"][0]["name"] == "Zenbook 14 OLED"


def test_get_product(client: TestClient) -> None:
    response = client.get("/products/2")

    assert response.status_code == 200
    assert response.json()["name"] == "ROG Zephyrus G14"


def test_get_missing_product(client: TestClient) -> None:
    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_search_by_name(client: TestClient) -> None:
    response = client.get("/products?q=rog")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert all("ROG" in item["name"] for item in body["items"])


def test_search_by_category(client: TestClient) -> None:
    response = client.get("/products?q=gaming")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert all("Gaming" in item["category"] for item in body["items"])


def test_sort_by_price_asc(client: TestClient) -> None:
    response = client.get("/products?sort=price&order=asc")

    assert response.status_code == 200
    prices = [item["price"] for item in response.json()["items"]]
    assert prices == sorted(prices)


def test_sort_by_name_desc(client: TestClient) -> None:
    response = client.get("/products?sort=name&order=desc")

    assert response.status_code == 200
    names = [item["name"] for item in response.json()["items"]]
    assert names == sorted(names, reverse=True)


def test_invalid_sort_returns_422(client: TestClient) -> None:
    response = client.get("/products?sort=id")

    assert response.status_code == 422


def test_invalid_order_returns_422(client: TestClient) -> None:
    response = client.get("/products?order=random")

    assert response.status_code == 422


def test_page_size_over_20_returns_422(client: TestClient) -> None:
    response = client.get("/products?page_size=21")

    assert response.status_code == 422


def test_pagination(client: TestClient) -> None:
    response = client.get("/products?page=1&page_size=2")

    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) == 2
    assert body["total"] == 6
    assert body["total_pages"] == 3
