import requests

# Базовый URL вашего приложения
BASE_URL = "http://127.0.0.1:8000"

def test_create_category():
    url = f"{BASE_URL}/categories/"
    payload = {"name": "Electronics"}
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Ошибка {response.status_code}: {response.text}"
    category = response.json()
    assert category["name"] == "Electronics"

def test_create_product():
    # Сначала создаем категорию
    category_response = requests.post(f"{BASE_URL}/categories/", json={"name": "Books"})
    assert category_response.status_code == 200
    category_id = category_response.json()["id"]

    # Теперь создаем продукт
    url = f"{BASE_URL}/products/"
    payload = {"name": "Python Book", "price": 500, "category_id": category_id}
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Ошибка {response.status_code}: {response.text}"
    product = response.json()
    assert product["name"] == "Python Book"
    assert product["price"] == 500
    assert product["category_id"] == category_id

def test_get_product():
    # Создаем категорию и продукт для тестирования
    category_response = requests.post(f"{BASE_URL}/categories/", json={"name": "Laptops"})
    assert category_response.status_code == 200
    category_id = category_response.json()["id"]

    product_response = requests.post(f"{BASE_URL}/products/", json={"name": "Gaming Laptop", "price": 1500, "category_id": category_id})
    assert product_response.status_code == 200
    product_id = product_response.json()["id"]

    # Получаем продукт по id
    url = f"{BASE_URL}/products/{product_id}"
    response = requests.get(url)
    assert response.status_code == 200, f"Ошибка {response.status_code}: {response.text}"
    product = response.json()
    assert product["id"] == product_id

def test_get_products():
    # Получаем список продуктов
    url = f"{BASE_URL}/products/"
    response = requests.get(url)
    assert response.status_code == 200, f"Ошибка {response.status_code}: {response.text}"
    products = response.json()
    assert isinstance(products, list)

def test_delete_product():
    # Сначала создаем категорию и продукт
    category_response = requests.post(f"{BASE_URL}/categories/", json={"name": "Tablets"})
    assert category_response.status_code == 200
    category_id = category_response.json()["id"]

    product_response = requests.post(f"{BASE_URL}/products/", json={"name": "iPad", "price": 800, "category_id": category_id})
    assert product_response.status_code == 200
    product_id = product_response.json()["id"]

    # Удаляем продукт
    url = f"{BASE_URL}/products/{product_id}"
    response = requests.delete(url)
    assert response.status_code == 200, f"Ошибка {response.status_code}: {response.text}"
    result = response.json()
    assert result["detail"] == "Product deleted"
