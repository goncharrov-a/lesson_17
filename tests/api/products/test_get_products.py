import json
import os

import allure
import pytest
import requests
from jsonschema import validate

BASE_URL = os.getenv("BASE_URL")


@allure.feature("Products")
@allure.story("Получение списка товаров")
@allure.title("Получение списка товаров возвращает 200 и валидную схему")
@allure.description("Проверка получения списка товаров и структуры ответа")
def test_get_all_products_success():
    with allure.step("Отправить GET запрос на /products"):
        response = requests.get(f"{BASE_URL}/products")

    with allure.step("Проверить, что статус код равен 200"):
        assert response.status_code == 200

    with allure.step("Проверить, что тело ответа является непустым списком"):
        body = response.json()
        assert isinstance(body, list)
        assert len(body) > 0

    with allure.step("Валидация схемы ответа"):
        with open("tests/schema/products.json") as schema_file:
            schema = json.load(schema_file)
        validate(body, schema)


@allure.feature("Products")
@allure.story("Получение списка товаров")
@allure.title("Запрос к несуществующему endpoint возвращает 404")
@allure.description("Негативный сценарий для GET /products")
def test_get_products_invalid_endpoint_returns_404():
    with allure.step("Отправить GET запрос на несуществующий endpoint"):
        response = requests.get(f"{BASE_URL}/products_invalid")

    with allure.step("Проверить, что статус код равен 404"):
        assert response.status_code == 404


@allure.feature("Products")
@allure.story("Получение товара по id")
@allure.title("Получение товара по id возвращает 200 и валидную схему")
@allure.description("Позитивный сценарий GET /products/{id}")
def test_get_product_by_id_success():
    product_id = 1

    with allure.step("Отправить GET запрос на /products/{id}"):
        response = requests.get(f"{os.getenv('BASE_URL')}/products/{product_id}")

    with allure.step("Проверить, что статус код равен 200"):
        assert response.status_code == 200

    with allure.step("Проверить, что id в ответе соответствует запрошенному"):
        body = response.json()
        assert body["id"] == product_id

    with allure.step("Валидация схемы ответа"):
        with open("tests/schema/product.json") as schema_file:
            schema = json.load(schema_file)
        validate(body, schema)


@allure.feature("Products")
@allure.story("Получение товара по id")
@allure.title("Запрос товара с несуществующим id возвращает пустое тело")
@allure.description("Негативный сценарий GET /products/{id} при отсутствии товара")
def test_get_product_by_invalid_id_returns_empty_body():
    invalid_product_id = 9999

    with allure.step("Отправить GET запрос на /products/{id} с несуществующим id"):
        response = requests.get(f"{os.getenv('BASE_URL')}/products/{invalid_product_id}")

    with allure.step("Проверить, что статус код равен 200"):
        assert response.status_code == 200

    with allure.step("Проверить, что тело ответа пустое"):
        assert response.text == ""


@pytest.mark.xfail(
    reason="API возвращает 200 и пустое тело вместо 404 для несуществующего товара",
    strict=True
)
@allure.feature("Products")
@allure.story("Получение товара по id")
@allure.title("Запрос товара с несуществующим id должен возвращать 404")
@allure.description(
    "Ожидаемое контрактное поведение: API должно возвращать 404, "
    "если товар не найден. Фактически API возвращает 200 и пустое тело."
)
def test_get_product_by_invalid_id_should_return_404():
    invalid_product_id = 9999

    with allure.step("Отправить GET запрос на /products/{id} с несуществующим id"):
        response = requests.get(f"{BASE_URL}/products/{invalid_product_id}")

    with allure.step("Проверить, что статус код равен 404"):
        assert response.status_code == 404
