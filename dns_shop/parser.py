import json
import logging
import sys
import time
from datetime import datetime

import psutil
import requests
import undetected_chromedriver as uc
from browsermobproxy import Server
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

from dns_shop.db.db import check_from_db

logging.basicConfig(format='%(asctime)s - %(levelname)s - [%(funcName)s]: %(message)s', level=logging.INFO,
                    datefmt='%d/%m/%y %H:%M:%S')


# todo добавить отображения url сообщении в тг

class DnsShop:

    def __init__(self, city):
        self.city = city
        self.url = 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/'

        self.cookies = self.get_cookies(city)

    def get_cookies(self, city='moscow'):
        logging.info('перехват cookies.')
        # путь до browser-mob-proxy
        path_proxy = "D:/python_projects/e-commerce_monitoring/tools/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat"

        # запускаем сервер
        server = Server(path_proxy)
        server.start()
        proxy = server.create_proxy()

        # добавляем опции для selenium
        options = Options()
        options.add_argument('--disable-bliwnk-features=AutomationControlled')
        options.add_argument('--proxy-server={0}'.format(proxy.proxy))  # передает proxy для перехвата запросов
        options.add_argument("--ignore-certificate-errors")  # игнорируем отсутствие ssl сертификата у proxy
        options.add_argument("--headless")  # отключаем графический интерфейс

        driver = uc.Chrome(options=options,
                           driver_executable_path='D:/python_projects/e-commerce_monitoring/tools/chromedriver-win64/chromedriver.exe')

        # service = Service(executable_path='D:/python_projects/e-commerce_monitoring/tools/chromedriver-win64/chromedriver.exe')
        # driver = webdriver.Chrome(service=service, options=options)

        # добавляем опции для перехвата запросов
        proxy.new_har("dns-shop", options={"captureCookies": True})

        # переходим на необходимый url
        driver.get(self.url)
        time.sleep(2)

        # записываем все запросы
        har = proxy.har

        # Просмотр cookies
        for entry in har['log']['entries']:
            request = entry['request']

            # достаем cookies для необходимого запроса
            if request['url'] == self.url:
                if request['cookies']:
                    qrator_jsid = request['cookies'][0]['value']
                    qrator_jsr = request['cookies'][1]['value']
                    qrator_ssid = request['cookies'][2]['value']

        server.stop()
        driver.quit()
        self.kill_process_server()

        # генерация cookies
        cookies = {
            'ipp_uid': '1654929432414/OkYNtCwXOhZj4i2W/h9rNBCwKAGhNFosfC/frHw==',
            '_ym_uid': '1654929432982921081',
            'rcuid': '62a438190bbf08000173aa84',
            '__ttl__widget__ui': '1655127727882-9cc1fe196b86',
            'rrpvid': '280683889390430',
            'tmr_lvid': '3d97f4bc781fc36f478aa83116f20cb9',
            'tmr_lvidTS': '1654929432319',
            'rrlevt': '1676794122158',
            'date-user-last-order-v2': 'b0ad3f9a22981fcba329b1a5ab681f63b8ba4cfd768cf4b09b1bcac6ea1e3925a%3A2%3A%7Bi%3A0%3Bs%3A23%3A%22date-user-last-order-v2%22%3Bi%3A1%3Bi%3A1676962660%3B%7D',
            'spid': '1678643560476_e53f038c8142d273eb84cea93eaa18f1_17sbhmgg6tbhrcbc',
            'ipp_sign': '45bcc4d63031aba2791767eb2ffea5a8_1143107671_9be2b7d22f00f8cda33988391b2c76dc',
            'ipp_key': 'v1683542158074/v33947245ba5adc7a72e273/v1pg9pZv1mgeWGmkIffLuA==',
            'phonesIdent': '52d633c91770fa5c021e34a3196166e6e61e0b9105465400a3ff988d935c2a38a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22phonesIdent%22%3Bi%3A1%3Bs%3A36%3A%22a19045b3-d7fa-4248-9ba8-5c8fc3b2b6f8%22%3B%7D',
            '_gcl_au': '1.1.1892688497.1687632832',
            '_ym_d': '1687632833',
            'configurationTutorialFinished': 'a204129f8e308b61d2cc5533331af3b5c8a6f96c3546a7f18b37a24e07723998a%3A2%3A%7Bi%3A0%3Bs%3A29%3A%22configurationTutorialFinished%22%3Bi%3A1%3Bi%3A1%3B%7D',
            'banners-hidden': '%7B%220871c555-3ae3-4e57-8b61-59061f84aae2%22%3A%5B%2217a8a01d-1640-11e5-a679-00259074e77d%22%5D%7D',
            'current_path': 'c78249a17e7537bea918aa2164bbcd7849b4d28ffa1b6cebb478e7d3f3fede19a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A109%3A%22%7B%22city%22%3A%2255506b51-0565-11df-9cf0-00151716f9f5%22%2C%22cityName%22%3A%22%5Cu0428%5Cu0430%5Cu0445%5Cu0442%5Cu044b%22%2C%22method%22%3A%22manual%22%7D%22%3B%7D',
            '_gid': 'GA1.2.2122640043.1691747485',
            '_ga_ND7GY87YET': 'GS1.1.1691934013.12.0.1691934109.60.0.0',
            'PHPSESSID': '3e86b4ab3b95eed1c2344dc61bf93f5f',
            'cartUserCookieIdent_v3': '3e5830ba1cc8e68ecf973cc75c89eec05c4ac9cde127a1463e54e91541cd8365a%3A2%3A%7Bi%3A0%3Bs%3A22%3A%22cartUserCookieIdent_v3%22%3Bi%3A1%3Bs%3A36%3A%22413f9f5d-ef80-365f-a48f-a3fc7360c3a1%22%3B%7D',
            '_ab_': '%7B%22catalog-hit-filter%22%3A%22favorites_analog_test%22%7D',
            '_ym_isad': '1',
            'lang': 'ru',
            '_csrf': '62828fa3d727d76996b2fac15ffe6cbe153b6baeb11b2880be2826e1bc8bbc31a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22ujcruIXEIcYXG2cyrhbpjXDow5AE5xlh%22%3B%7D',
            'city_path': city,
            '_ga': 'GA1.2.175639799.1654929432',
            'tmr_detect': '1%7C1692112724633',
            'qrator_ssid': qrator_ssid,
            'qrator_jsr': qrator_jsr,
            '_ga_FLS4JETDHW': 'GS1.1.1692134197.204.0.1692134197.60.0.0',
            'qrator_jsid': qrator_jsid,
        }

        logging.info(f'Cookies получены CITY:{city.upper()}')
        return cookies

    def kill_process_server(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'java.exe':
                # Завершаем процесс Java
                proc.kill()

    def get_html_content(self, page=1):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            # 'Cookie': 'ipp_uid=1654929432414/OkYNtCwXOhZj4i2W/h9rNBCwKAGhNFosfC/frHw==; _ym_uid=1654929432982921081; rcuid=62a438190bbf08000173aa84; __ttl__widget__ui=1655127727882-9cc1fe196b86; rrpvid=280683889390430; tmr_lvid=3d97f4bc781fc36f478aa83116f20cb9; tmr_lvidTS=1654929432319; rrlevt=1676794122158; date-user-last-order-v2=b0ad3f9a22981fcba329b1a5ab681f63b8ba4cfd768cf4b09b1bcac6ea1e3925a%3A2%3A%7Bi%3A0%3Bs%3A23%3A%22date-user-last-order-v2%22%3Bi%3A1%3Bi%3A1676962660%3B%7D; spid=1678643560476_e53f038c8142d273eb84cea93eaa18f1_17sbhmgg6tbhrcbc; ipp_sign=45bcc4d63031aba2791767eb2ffea5a8_1143107671_9be2b7d22f00f8cda33988391b2c76dc; ipp_key=v1683542158074/v33947245ba5adc7a72e273/v1pg9pZv1mgeWGmkIffLuA==; phonesIdent=52d633c91770fa5c021e34a3196166e6e61e0b9105465400a3ff988d935c2a38a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22phonesIdent%22%3Bi%3A1%3Bs%3A36%3A%22a19045b3-d7fa-4248-9ba8-5c8fc3b2b6f8%22%3B%7D; _gcl_au=1.1.1892688497.1687632832; _ym_d=1687632833; configurationTutorialFinished=a204129f8e308b61d2cc5533331af3b5c8a6f96c3546a7f18b37a24e07723998a%3A2%3A%7Bi%3A0%3Bs%3A29%3A%22configurationTutorialFinished%22%3Bi%3A1%3Bi%3A1%3B%7D; banners-hidden=%7B%220871c555-3ae3-4e57-8b61-59061f84aae2%22%3A%5B%2217a8a01d-1640-11e5-a679-00259074e77d%22%5D%7D; current_path=c78249a17e7537bea918aa2164bbcd7849b4d28ffa1b6cebb478e7d3f3fede19a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A109%3A%22%7B%22city%22%3A%2255506b51-0565-11df-9cf0-00151716f9f5%22%2C%22cityName%22%3A%22%5Cu0428%5Cu0430%5Cu0445%5Cu0442%5Cu044b%22%2C%22method%22%3A%22manual%22%7D%22%3B%7D; _gid=GA1.2.2122640043.1691747485; _ga_ND7GY87YET=GS1.1.1691934013.12.0.1691934109.60.0.0; _ym_isad=1; profile_dnsauth_csrf=57d6bff629c0249d92e3ebbcfa65db2b450fae4dba14ce196df050ecfee39b25a%3A2%3A%7Bi%3A0%3Bs%3A20%3A%22profile_dnsauth_csrf%22%3Bi%3A1%3Bs%3A36%3A%221829455e-2482-435c-a535-e536ab135240%22%3B%7D; PHPSESSID=3e86b4ab3b95eed1c2344dc61bf93f5f; cartUserCookieIdent_v3=3e5830ba1cc8e68ecf973cc75c89eec05c4ac9cde127a1463e54e91541cd8365a%3A2%3A%7Bi%3A0%3Bs%3A22%3A%22cartUserCookieIdent_v3%22%3Bi%3A1%3Bs%3A36%3A%22413f9f5d-ef80-365f-a48f-a3fc7360c3a1%22%3B%7D; lang=ru; _csrf=0651a7ccafb90b74d00e52c2d380c0bb0f025d285cab7ac16fab5b7d0c37d4a0a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22OEiJkbmlLZloA3-CuJnGm-TWD4svohlV%22%3B%7D; city_path=shakhty; qrator_jsid=1692050867.983.e5zwcXrfemzyh3wo-62o1v5qfajq7b84q59jsl4mtan3q5qne; _ym_visorc=b; tmr_detect=1%7C1692051845520; _ga=GA1.2.175639799.1654929432; _ga_FLS4JETDHW=GS1.1.1692050870.197.1.1692052241.60.0.0',
            'Referer': 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?p=6',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'X-CSRF-Token': 'vaTsbw6lA3tfXlLz8kMGwXzNHKpUaWa3L8_0L6mpgr7y4YUlZcduFxMEPpyzcCuCCYdy7TlEMuBr-4dZxsHu6A==',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        params = {
            'p': page,
        }

        response = requests.get(
            self.url,
            params=params,
            cookies=self.cookies,
            headers=headers,
        )

        if response.status_code == 401:
            self.cookies = self.get_cookies("shakhty")

        response = requests.get(
            self.url,
            params=params,
            cookies=self.cookies,
            headers=headers,
        )

        try:
            response_json = response.json()
            html_content = response_json['html']

            return html_content

        except Exception as ex:
            logging.error('[__ERROR__] Не удалось вернуть html контент.', response.status_code)

    def get_data_page(self, page=1):
        html_content = self.get_html_content(page)
        soup = BeautifulSoup(html_content, 'lxml')

        products = soup.find_all(attrs={"data-id": "product"})

        product_ids = []
        product_data_ids = []

        for product in products:
            product_id = product.find('span', class_='catalog-product__buy product-buy').get('id')
            product_data_id = product.get('data-code')

            product_ids.append(product_id)
            product_data_ids.append(product_data_id)

        return product_ids, product_data_ids

    def post_data(self, data):
        headers = {
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'content-type': 'application/x-www-form-urlencoded',
            'Referer': 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/no-referrer',
            'X-CSRF-Token': 'yX83jHQj6m9r0D3zhh9aj-BApwNzai9nEpdjPdEPu5eCJg7tLHGsFlqDS5nCUTzDjyTkViEORz1LzzJoiDeD4w==',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        response = requests.post('https://www.dns-shop.ru/ajax-state/product-buy/', headers=headers, data=data)

        response_json = response.json()

        return response_json

    def get_pagination(self):
        page = 1
        while True:
            html_content = self.get_html_content(page=page)
            soup = BeautifulSoup(html_content, 'lxml')
            result = True if soup.find('button', class_='pagination-widget__show-more-btn') else False
            if not result:
                logging.info(f'Всего страниц в категории: {page}')
                return page
            page += 1

    def get_product_info(self):
        pages = self.get_pagination()
        for page in range(1, pages + 1):
            product_ids, product_data_ids = self.get_data_page(page)

            data = {
                "type": "product-buy",
                "containers": [
                    {
                        "id": product_id,
                        "data": {
                            "id": product_data_id
                        }
                    }
                    for product_id, product_data_id in zip(product_ids, product_data_ids)
                ]
            }

            data = 'data=' + str(data)
            data = data.replace("'", '"')

            response_json = self.post_data(data)

            products = response_json['data']['states']

            now = datetime.now()
            date = now.strftime("%d-%m-%Y %H:%M")

            for product in products:
                title = product['data']['name']
                price = product['data']['price']['current']

                check_from_db(title, price, date)

            logging.info(f'{page}/{pages}')

    def check_changes(self, url=None):
        if url:
            self.url = url

        self.get_product_info()
