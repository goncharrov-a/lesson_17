import json
import os

import allure
import requests
from jsonschema import validate


@allure.feature("Products")
@allure.story("Обновление товара")
@allure.title("Обновление товара возвращает 200 и валидную схему")
@allure.description("Позитивный сценарий PUT /products/{id}")
def test_update_product_success():
    product_id = 1
    payload = {
        "title": "Updated product",
        "price": 199.99,
        "description": "Updated description",
        "category": "electronics",
        "image": "https://example.com/updated.png"
    }

    with allure.step("Отправить PUT запрос на /products/{id} с валидным телом"):
        response = requests.put(
            f"{os.getenv('BASE_URL')}/products/{product_id}",
            json=payload
        )

    with allure.step("Проверить, что статус код равен 200"):
        assert response.status_code == 200

    with allure.step("Проверить, что данные товара обновлены"):
        body = response.json()
        assert body["title"] == payload["title"]
        assert body["price"] == payload["price"]

    with allure.step("Валидация схемы ответа"):
        with open("tests/schema/product.json") as schema_file:
            schema = json.load(schema_file)
        validate(body, schema)


@allure.feature("Products")
@allure.story("Обновление товара")
@allure.title("Обновление товара без тела запроса должно возвращать 400")
@allure.description(
    "Expected: API должно валидировать тело запроса и возвращать 400. "
    "Fact: API возвращает 200 и обновляет товар некорректно."
)
def test_update_product_without_body_should_return_400():
    product_id = 1

    with allure.step("Отправить PUT запрос на /products/{id} без тела"):
        response = requests.put(f"{os.getenv('BASE_URL')}/products/{product_id}")

    with allure.step("Проверить, что статус код равен 400"):
        assert response.status_code == 400