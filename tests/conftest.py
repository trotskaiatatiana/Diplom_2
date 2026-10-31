
import allure
import pytest
import requests

from helpers import generate_user_data
from urls import Urls


@pytest.fixture
def created_user():
    with allure.step("Создать уникального пользователя"):
        user_data = generate_user_data()
        response = requests.post(
            Urls.REGISTER_URL,
            json=user_data,
            timeout=10
        )

        assert response.status_code == 200
        token = response.json()["accessToken"]

    yield user_data, response

    with allure.step("Удалить тестового пользователя"):
        delete_response = requests.delete(
            Urls.USER_URL,
            headers={"Authorization": token},
            timeout=10
        )
        assert delete_response.status_code == 202


@pytest.fixture
def ingredient_ids():
    with allure.step("Получить список ингредиентов"):
        response = requests.get(
            Urls.INGREDIENTS_URL,
            timeout=10
        )

        assert response.status_code == 200

        ingredients = response.json()["data"]

        return [ingredients[0]["_id"], ingredients[1]["_id"]]
