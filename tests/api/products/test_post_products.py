import json
import os

import allure
import requests
from jsonschema import validate


@allure.feature("Products")
@allure.story("Создание товара")
@allure.title("Создание товара возвращает 201 и валидную схему")
@allure.description("Позитивный сценарий POST /products")
def test_create_product_success():
    payload = {
        "title": "Test product",
        "price": 99.99,
        "description": "Test description",
        "category": "electronics",
        "image": "https://example.com/image.png"
    }

    with allure.step("Отправить POST запрос на /products с валидным телом"):
        response = requests.post(
            f"{os.getenv('BASE_URL')}/products",
            json=payload
        )

    with allure.step("Проверить, что статус код равен 201"):
        assert response.status_code == 201

    with allure.step("Проверить, что данные товара совпадают с отправленными"):
        body = response.json()
        assert body["title"] == payload["title"]
        assert body["price"] == payload["price"]

    with allure.step("Валидация схемы ответа"):
        with open("tests/schema/product.json") as schema_file:
            schema = json.load(schema_file)
        validate(body, schema)


@allure.feature("Products")
@allure.story("Создание товара")
@allure.title("Создание товара без обязательных полей должно возвращать 400")
@allure.description(
    "Expected: API должно валидировать тело запроса и возвращать 400. "
    "Fact: API возвращает 201 и создаёт некорректный товар."
)
def test_create_product_without_body_should_return_400():
    with allure.step("Отправить POST запрос на /products без тела"):
        response = requests.post(f"{os.getenv('BASE_URL')}/products")

    with allure.step("Проверить, что статус код равен 400"):
        assert response.status_code == 400


@allure.feature("Products")
@allure.story("Получение товара по id")
@allure.title("Запрос товара с невалидным id должен возвращать 400")
@allure.description(
    "Expected: API должно возвращать 400 при невалидном id согласно документации. "
    "Fact: API возвращает 200 и пустое тело."
)
def test_get_product_with_invalid_id_should_return_400():
    invalid_product_id = "abc"

    with allure.step("Отправить GET запрос на /products/{id} с невалидным id"):
        response = requests.get(f"{'BASE_URL'}/products/{invalid_product_id}")

    with allure.step("Проверить, что статус код равен 400"):
        assert response.status_code == 400
