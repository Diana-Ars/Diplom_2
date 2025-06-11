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
    print(user)
    response = UserMethods.login_user(email=user['email'], password=user['password'])
    print(response)
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
def create_fix_user():
    user_data = generate_user_body()
    user_data['email'] = 'fix_email@email.com'
    UserMethods.create_user(user_data)
    user = {'email': user_data['email'], 'name': user_data['name'], 'password':user_data['password']}
    yield user


@pytest.fixture
def auth_user_and_create_order(auth_user):
    order = OrderMethods.create_order(Data.fix_order_body, auth_user['headers'])
    yield {'auth_user': auth_user, 'order': order}


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
    yield {'auth_user': auth_user, 'orders': orders}

@pytest.fixture
def auth_user_with_refresh_token():
    user_data = generate_user_body()
    UserMethods.create_user(user_data)
    user = {'email': user_data['email'], 'name': user_data['name'], 'password': user_data['password']}
    print(user)
    response = UserMethods.login_user(email=user['email'], password=user['password'])
    print(response)
    token = response.json().get('accessToken')
    refresh_token = response.json().get('refreshToken')
    if response.status_code == 200 and token:
        auth_user = {
            'email': user_data['email'],
            'name': user_data['name'],
            'accessToken': token,
            'refreshToken': refresh_token,
            'headers': {
                'Authorization': token
            }
        }
        yield auth_user
    else:
        pytest.fail(f"Ошибка при логине: {response.status_code}")
        if refresh_token:
            new_token_response = UserMethods.refresh_token(body={'token': refresh_token})
            if new_token_response.status_code == 200:
                token = new_token_response.json().get('accessToken')
                if not token:
                    pytest.fail("Не получен accessToken при обновлении токена")

                auth_user = {
                    'email': user_data['email'],
                    'name': user_data['name'],
                    'accessToken': token,
                    'refreshToken': refresh_token,
                    'headers': {
                        'Authorization': token
                    }
                }
                yield auth_user
            else:
                pytest.fail(f"Ошибка при обновлении токена: {new_token_response.status_code}")
        else:
            pytest.fail("Не получен refreshToken при логине")

        UserMethods.delete_user(user['name'])

