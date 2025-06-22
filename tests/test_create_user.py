import allure
import pytest

from user_methods import UserMethods
from helpers import *
from data import Data


class TestCreateUser:
    @allure.title('Проверка успешного создания пользователя при заполнении всех полей')
    def test_success_create_user(self):
        user_data = generate_user_body()
        with allure.step('Создание пользователя'):
            creation = UserMethods.create_user(user_data)
        assert creation.status_code == 200 and creation.json()['success'] == True

    @allure.title('Проверка неуспешного создания пользователя при создании дубля')
    def test_failed_create_user_double(self):
        user_data = generate_user_body()
        with allure.step('Создание пользователя'):
            creation = UserMethods.create_user(user_data)
        with allure.step('Создание дубля пользователя'):
            double_creation = UserMethods.create_user(user_data)
        assert double_creation.status_code == 403 and double_creation.json()['message'] == Data.error_message_double_user

    @allure.title('Проверка неуспешного создания пользователя при пустом вводе значения "{param}"')
    @pytest.mark.parametrize('param', ['email', 'password', 'name'])
    def test_failed_create_user_when_field_is_empty(self, param):
        user_data = generate_user_body()
        user_data[param] = Data.empty_param
        with allure.step('Создание пользователя'):
            creation = UserMethods.create_user(user_data)
        assert creation.status_code == 403 and creation.json()['message'] == Data.error_message_create_user

    @allure.title('Проверка неуспешного создания пользователя при отсутствии "{missing_field}" в теле запроса')
    @pytest.mark.parametrize('missing_field', [
        ['email'],
        ['password'],
        ['name'],
        ['email', 'password', 'name']
        ]
                             )
    def test_failed_create_user_without_field_in_body(self, missing_field):
        user_data = generate_user_body()
        missing_data = create_user_body_without_fields(missing_field, user_data)
        with allure.step('Создание пользователя'):
            creation = UserMethods.create_user(missing_data)
        assert creation.status_code == 403 and creation.json()['message'] == Data.error_message_create_user

    @allure.title('Проверка неуспешного создания пользователя при пустом теле запроса')
    def test_failed_create_user_when_body_empty(self):
        with allure.step('Создание пользователя'):
            creation = UserMethods.create_user(body='')
        assert creation.status_code == 403 and creation.json()['message'] == Data.error_message_create_user

