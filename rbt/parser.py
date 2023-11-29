import json
import logging
import time
from datetime import datetime

from rbt.db.db import check_from_db
from utils.functions import send_message

import requests

logging.basicConfig(format='%(asctime)s - %(levelname)s - [%(funcName)s]: %(message)s', level=logging.INFO,
                    datefmt='%d/%m/%y %H:%M:%S')


class Rbt:
    def get_api_response(self):
        headers = {
            'authority': 'api.retailrocket.ru',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://shakhty.rbt.ru',
            'referer': 'https://shakhty.rbt.ru/',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }

        response = requests.get(
            'https://api.retailrocket.ru/api/2.0/recommendation/personal/compositeForCategory/54e2c43c1e99470d5c66f56a/?&categoryIds=91&stockId=1108&algorithmType=personal&session=62a438190bbf08000173aa84&pvid=991619821452901&isDebug=false&format=json',
            headers=headers,
        )

        return response.json()

    def save_api_data(self):
        products = self.get_api_response()

        now = datetime.now()
        date = now.strftime("%d-%m-%Y %H:%M")

        for product in products:
            title = product['Model']
            price = product['Price']
            url = product['Url']

            check_from_db(title, price, date, url)

        logging.info('получены новые данные о товарах RBT.RU')

    def check_changes(self):
        self.save_api_data()
        # self.compare_json_file()
