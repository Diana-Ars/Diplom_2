import allure
import pytest

from user_methods import UserMethods
from data import Data
from helpers import *


class TestLoginUser:
    @allure.title('Проверка успешной авторизации существующего пользователя')
    def test_success_login(self, create_user):
        user = create_user
        with allure.step('Авторизация пользователя'):
            response = UserMethods.login_user(email=user['email'], password=user['password'])
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Проверка неуспешной авторизации с несуществующим "{param}"')
    @pytest.mark.parametrize('param', ['email', 'password'])
    def test_failed_login_with_fake_param(self, create_user, param):
        user_data = create_user
        user_data[param] = Data.fake_param
        with allure.step('Авторизация пользователя'):
            response = UserMethods.login_user(user_data['email'], user_data['password'])
        assert response.status_code == 401 and response.json()['success'] == False

    @allure.title('Проверка неуспешной авторизации с пустым полем "{param}"')
    @pytest.mark.parametrize('param', ['email', 'password', 'both'])
    def test_failed_login_with_empty_param(self, create_user, param):
        user_data = create_user
        data_with_empty = generate_user_body_with_empty_params(param, user_data)
        with allure.step('Авторизация пользователя'):
            response = UserMethods.login_user(data_with_empty['email'], data_with_empty['password'])
        assert response.status_code == 401 and response.json()['success'] == False

    @allure.title('Проверка неуспешной авторизации при отсутствии "{missing_field}" в теле запроса')
    @pytest.mark.parametrize('missing_field', [
        ['email'],
        ['password'],
        ['email', 'password']
    ]
                             )
    def test_failed_login_user_when_field_missing(self, create_user, missing_field):
        user_data = create_user
        data_without_fields = login_user_body_without_fields(missing_field, user_data)
        with allure.step('Авторизация пользователя'):
            response = UserMethods.login_user(body=data_without_fields)
        assert response.status_code == 401

    @allure.title('Проверка неуспешной авторизации при отсутствии тела запроса')
    def test_failed_login_user_when_body_empty(self, create_user):
        with allure.step('Авторизация пользователя'):
            response = UserMethods.login_user(body='')
        assert response.status_code == 400

