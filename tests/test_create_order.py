import pytest
import allure
from order_methods import OrderMethods
from data import *


class TestCreateOrder:
    @allure.title('Проверка успешного создания заказа с авторизацией пользователя')
    def test_success_create_order_with_login(self, auth_user):
        with allure.step('Создание заказа'):
            response = OrderMethods.create_order(Data.fix_order_body, auth_user['headers'])
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Проверка успешного создания заказа с ингредиентами')
    def test_success_create_order_with_ingredients(self, auth_user):
        with allure.step('Создание заказа'):
            response = OrderMethods.create_order(Data.fix_order_body, auth_user['headers'])
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Проверка неуспешного создания заказа без авторизации пользователя')
    def test_failed_create_order_without_login(self, auth_user):
        with allure.step('Создание заказа'):
            response = OrderMethods.create_order(Data.fix_order_body, {'Authorization': ''})
        assert response.status_code == 400 and response.json()['success'] == False

    @allure.title('Проверка неуспешного создания заказа с пустым телом запроса')
    def test_failed_create_order_without_ingredients(self, auth_user):
        with allure.step('Создание заказа'):
            response = OrderMethods.create_order(Data.empty_order_body, auth_user['headers'])
        assert response.status_code == 400 and response.json()['success'] == False

    @allure.title('Проверка неуспешного создания заказа с пустым списком ингредиентов')
    def test_failed_create_order_without_ingredients(self, auth_user):
        with allure.step('Создание заказа'):
            response = OrderMethods.create_order(Data.empty_order_body_list, auth_user['headers'])
        assert response.status_code == 400 and response.json()['message'] == Data.error_message_create_order

    @allure.title('Проверка неуспешного создания заказа с несуществующим хешем ингредиента')
    def test_failed_create_order_with_fake_hash_of_ingredient(self, auth_user):
        with allure.step('Создание заказа'):
            response = OrderMethods.create_order(Data.fake_hash_order_body, auth_user['headers'])
        assert response.status_code == 500  # согласно документации возвращается только код ответа

