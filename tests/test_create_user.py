import allure
import pytest
import requests

from helpers import generate_user_data
from urls import Urls


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user(self, created_user):
        user_data, response = created_user

        with allure.step("Проверить успешную регистрацию"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert response.json()["user"]["email"] == user_data["email"]
            assert response.json()["user"]["name"] == user_data["name"]
            assert "accessToken" in response.json()
            assert "refreshToken" in response.json()

    @allure.title("Нельзя создать уже зарегистрированного пользователя")
    def test_create_existing_user(self, created_user):
        user_data, _ = created_user

        with allure.step("Повторно зарегистрировать пользователя"):
            response = requests.post(
                Urls.REGISTER_URL,
                json=user_data,
                timeout=10
            )

        with allure.step("Проверить ошибку регистрации"):
            assert response.status_code == 403
            assert response.json()["success"] is False
            assert response.json()["message"] == "User already exists"

    
    @allure.title("Нельзя создать пользователя без поля {field}")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, field):
        user_data = generate_user_data()
        user_data.pop(field)

        with allure.step(f"Зарегистрировать пользователя без поля {field}"):
            response = requests.post(
                Urls.REGISTER_URL,
                json=user_data,
                timeout=10
            )

        with allure.step("Проверить ошибку регистрации"):
            assert response.status_code == 403
            assert response.json()["success"] is False
            assert response.json()["message"] == (
                "Email, password and name are required fields"
            )