import pytest
import allure

from order_methods import OrderMethods
from data import *


class TestGetOrder:
    @allure.title('Проверка успешного получения списка заказов при формировании 1 заказа')
    def test_success_get_order_by_user(self, auth_user_and_create_order):
        with allure.step('Получение списка заказов'):
            response = OrderMethods.get_order_by_user(auth_user_and_create_order['auth_user']['headers'])
        assert response.status_code == 200 and response.json()['success']
        assert response.json()['total'] == 1

    @allure.title('Проверка успешного получения списка из 50 заказов')  #из-за большого количества создаваемых заказов, тест долгий
    def test_success_get_50_orders_by_user(self, auth_user_and_create_50_orders):
        with allure.step('Получение списка заказов'):
            response = OrderMethods.get_order_by_user(auth_user_and_create_50_orders['auth_user']['headers'])
        assert response.status_code == 200 and response.json()['success']
        assert response.json()['total'] == 50

    @allure.title('Проверка неуспешного получения списка заказов без авторизации')
    def test_failed_get_order_without_login(self, auth_user_and_create_order):
        with allure.step('Получение списка заказов'):
            response = OrderMethods.get_order_by_user({'Authorization': ''})
        assert response.status_code == 401 and response.json()['message'] == Data.error_message_not_auth

