import pytest
from helpers import *
from user_methods import UserMethods
from order_methods import OrderMethods
from data import *
import random


@pytest.fixture
def create_user():
    user_data = generate_user_body()
    UserMethods.create_user(user_data)
    user = {'email': user_data['email'], 'name': user_data['name'], 'password':user_data['password']}
    yield user
    UserMethods.delete_user(user['name'])

@pytest.fixture
def auth_user():
    user_data = generate_user_body()
    UserMethods.create_user(user_data)
    user = {'email': user_data['email'], 'name': user_data['name'], 'password': user_data['password']}
    response = UserMethods.login_user(email=user['email'], password=user['password'])
    if response.status_code != 200:
        pytest.fail(f"Ошибка при логине: {response.status_code}")
    token = response.json().get('accessToken')
    if not token:
        pytest.fail("Не получен accessToken при логине")
    auth_user = {
        'email': user_data['email'],
        'name': user_data['name'],
        'accessToken': token,
        'headers': {
            'Authorization': token
        }
    }
    yield auth_user
    UserMethods.delete_user(user['name'])

@pytest.fixture
def auth_user_and_create_order(auth_user):
    order = OrderMethods.create_order(Data.fix_order_body, auth_user['headers'])
    return {'auth_user': auth_user, 'order': order}

@pytest.fixture
def auth_user_and_create_50_orders(auth_user):
    ingredients_response = OrderMethods.get_info_about_ingredients()
    ingredients = ingredients_response.json()
    ingredient_ids = [ingredient['_id'] for ingredient in ingredients['data']]
    orders = []
    for _ in range(50):
        selected_ingredients = random.sample(ingredient_ids, k=min(3, len(ingredient_ids)))
        order_body = Data.fix_order_body.copy()
        order_body['ingredients'] = selected_ingredients
        order = OrderMethods.create_order(order_body,auth_user['headers']).json()
        orders.append(order)
    return {'auth_user': auth_user, 'orders': orders}

