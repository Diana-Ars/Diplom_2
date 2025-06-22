import allure
import pytest
from user_methods import UserMethods
from helpers import *
from data import *


class TestChangeUserData:
    @allure.title('Проверка успешного изменения данных пользователя с авторизацией')
    @pytest.mark.parametrize('param', ['both', 'email', 'name'])
    def test_success_change_user_data_(self, auth_user, param):
        data = auth_user
        new_data = generate_user_body_with_fake_params(param, data)
        with allure.step('Изменение данных пользователя'):
            response = UserMethods.change_user_data(auth_user['headers'], new_data)
        assert response.status_code == 200

    @allure.title('Проверка неуспешного изменения данных пользователя без авторизации')
    @pytest.mark.parametrize('param', ['both', 'email', 'name'])
    def test_failed_change_user_data_without_login(self, create_user, param):
        data = create_user
        new_data = generate_user_body_with_fake_params(param, data)
        with allure.step('Изменение данных пользователя'):
            response = UserMethods.change_user_data({'Authorization': ''}, new_data)
        assert response.status_code == 401 and response.json()['message'] == Data.error_message_not_auth

    @allure.title('Проверка неуспешного изменения данных пользователя при повторяющемся email')
    def test_failed_change_user_data_double_email(self, auth_user):
        fix_user_data = auth_user
        fix_user_data['email'] = Data.fix_email
        with allure.step('Создание пользователя'):
            UserMethods.create_user(fix_user_data)
        new_data = {
            'email': fix_user_data['email'],
            'name': auth_user['name']
        }
        with allure.step('Изменение данных пользователя'):
            response = UserMethods.change_user_data(auth_user['headers'], new_data)
        assert response.status_code == 403 and response.json()['message'] == Data.error_message_double_email

