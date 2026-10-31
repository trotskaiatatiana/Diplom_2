
import allure
import pytest
import requests

from urls import Urls


@allure.feature("Авторизация пользователя")
class TestLoginUser:

    @allure.title("Успешная авторизация пользователя")
    def test_login_existing_user(self, created_user):
        user_data, _ = created_user

        with allure.step("Авторизоваться с корректными данными"):
            response = requests.post(
                Urls.LOGIN_URL,
                json=user_data,
                timeout=10
            )

        with allure.step("Проверить успешную авторизацию"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert response.json()["user"]["email"] == user_data["email"]
            assert response.json()["user"]["name"] == user_data["name"]
            assert "accessToken" in response.json()
            assert "refreshToken" in response.json()

    @allure.title("Авторизация с некорректным полем {field}")
    @pytest.mark.parametrize("field", ["email", "password"])
    def test_login_with_invalid_credentials(self, created_user, field):
        user_data, _ = created_user
        invalid_data = user_data.copy()
        invalid_data[field] = "invalid_value"

        with allure.step(f"Авторизоваться с некорректным полем {field}"):
            response = requests.post(
                Urls.LOGIN_URL,
                json=invalid_data,
                timeout=10
            )

        with allure.step("Проверить ошибку авторизации"):
            assert response.status_code == 401
            assert response.json()["success"] is False
            assert response.json()["message"] == (
                "email or password are incorrect"
            )
