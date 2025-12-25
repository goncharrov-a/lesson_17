import os

import allure
import requests


@allure.feature("Products")
@allure.story("Удаление товара")
@allure.title("Удаление товара возвращает 200")
@allure.description("Позитивный сценарий DELETE /products/{id}")
def test_delete_product_success():
    product_id = 1

    with allure.step("Отправить DELETE запрос на /products/{id}"):
        response = requests.delete(
            f"{os.getenv('BASE_URL')}/products/{product_id}"
        )

    with allure.step("Проверить, что статус код равен 200"):
        assert response.status_code == 200
