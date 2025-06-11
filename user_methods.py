import requests
from helpers import *
from curl import Url

class UserMethods:
    @staticmethod
    def create_user(body):
        return requests.post(f'{Url.CREATE_USER}', json=body)

    @staticmethod
    def login_user(email=None, password=None, body=None):
        if body is not None:
            return requests.post(f'{Url.LOGIN}', json=body)
        elif email is not None and password is not None:
            params = {'email': email, 'password': password}
            return requests.post(f'{Url.LOGIN}', json=params)
        else:
            return requests.post(f'{Url.LOGIN}', json={})

    @staticmethod
    def delete_user(user):
        return requests.delete(f'{Url.DELETE_USER}/{user}')

    @staticmethod
    def change_user_data(headers, new_data):
        return requests.patch(f'{Url.INFO_USER}', headers=headers, json=new_data)

    @staticmethod
    def get_user_info():
        return requests.get(f'{Url.INFO_USER}')

    @staticmethod
    def refresh_token(body):
        return requests.post(f'{Url.TOKEN}', json=body)