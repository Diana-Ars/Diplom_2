import requests
from curl import Url


class OrderMethods:
    @staticmethod
    def get_info_about_ingredients():
        return requests.get(f'{Url.BASE_URL}/ingredients')

    @staticmethod
    def create_order(body, headers):
        return requests.post(f'{Url.CREATE_ORDER}', json=body, headers=headers)

    @staticmethod
    def get_order_by_user(headers):
        return requests.get(f'{Url.CREATE_ORDER}', headers=headers)

