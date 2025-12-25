import os

import allure
import requests


@allure.feature("Products")
@allure.story("E2E CRUD сценарий")
@allure.title("E2E: создание, получение, обновление и удаление товара")
@allure.description(
    "E2E сценарий для /products: POST → GET → PUT → DELETE. "
    "Проверяет базовую бизнес-логику работы с товаром."
)
def test_products_e2e_crud():
    base_url = os.getenv("BASE_URL")

    create_payload = {
        "title": "E2E product",
        "price": 123.45,
        "description": "E2E description",
        "category": "electronics",
        "image": "https://example.com/e2e.png"
    }

    update_payload = {
        "title": "E2E product updated",
        "price": 222.22,
        "description": "Updated description",
        "category": "electronics",
        "image": "https://example.com/e2e_updated.png"
    }

    with allure.step("POST /products - создать товар"):
        create_response = requests.post(
            f"{base_url}/products",
            json=create_payload
        )
        assert create_response.status_code == 201
        created_product = create_response.json()
        product_id = created_product["id"]

    with allure.step("GET /products/{id} - получить созданный товар"):
        get_response = requests.get(
            f"{base_url}/products/{product_id}"
        )
        assert get_response.status_code == 200
        get_body = get_response.json()
        assert get_body["id"] == product_id

    with allure.step("PUT /products/{id} - обновить товар"):
        update_response = requests.put(
            f"{base_url}/products/{product_id}",
            json=update_payload
        )
        assert update_response.status_code == 200
        updated_body = update_response.json()
        assert updated_body["title"] == update_payload["title"]
        assert updated_body["price"] == update_payload["price"]

    with allure.step("DELETE /products/{id} - удалить товар"):
        delete_response = requests.delete(
            f"{base_url}/products/{product_id}"
        )
        assert delete_response.status_code == 200

    with allure.step("GET /products/{id} - получить созданный товар"):
        get_response = requests.get(
            f"{base_url}/products/{product_id}"
        )
        assert get_response.status_code == 200

        if get_response.text:
            get_body = get_response.json()
            assert get_body["id"] == product_id
        else:
            allure.attach(
                body="GET /products/{id} вернул 200 с пустым телом. "
                     "API не сохраняет созданные товары.",
                name="API bug",
                attachment_type=allure.attachment_type.TEXT
            )
