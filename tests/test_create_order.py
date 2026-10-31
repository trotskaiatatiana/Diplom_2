
import allure
import requests

from urls import Urls


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth(self, created_user, ingredient_ids):
        _, register_response = created_user
        token = register_response.json()["accessToken"]

        with allure.step("Отправить запрос на создание заказа"):
            response = requests.post(
                Urls.ORDERS_URL,
                json={"ingredients": ingredient_ids},
                headers={"Authorization": token},
                timeout=10
            )

        with allure.step("Проверить успешное создание заказа"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "number" in response.json()["order"]

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, ingredient_ids):
        with allure.step("Отправить запрос без токена"):
            response = requests.post(
                Urls.ORDERS_URL,
                json={"ingredients": ingredient_ids},
                timeout=10
            )

        with allure.step("Проверить ответ сервера"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "order" in response.json()
            assert "number" in response.json()["order"]

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        with allure.step("Отправить запрос с пустым списком ингредиентов"):
            response = requests.post(
                Urls.ORDERS_URL,
                json={"ingredients": []},
                timeout=10
            )

        with allure.step("Проверить ошибку"):
            assert response.status_code == 400
            assert response.json()["success"] is False
            assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с некорректным хешем ингредиента")
    def test_create_order_with_invalid_ingredient(self):
        with allure.step("Отправить запрос с некорректным хешем"):
            response = requests.post(
                Urls.ORDERS_URL,
                json={"ingredients": ["invalid_hash"]},
                timeout=10
            )

        with allure.step("Проверить ошибку"):
            assert response.status_code == 500
