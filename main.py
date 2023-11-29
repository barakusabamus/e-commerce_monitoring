import time
import logging

from dns_shop.parser import DnsShop
from rbt.parser import Rbt
from utils.functions import send_message

logging.basicConfig(format='%(asctime)s - %(levelname)s - [%(funcName)s]: %(message)s', level=logging.INFO,
                    datefmt='%d/%m/%y %H:%M:%S')


# todo отображать процент или сумму изменения цены
# todo Добавить мвидео ситилинк онлайн трейд
# todo Добавить озон ям вб сбер
def monitoring():
    city = 'shakhty'

    rbt = Rbt()
    dns_shops = DnsShop(city=city)

    while True:

        try:
            dns_shops.check_changes()
            # dns_shops.check_changes(
            #     'https://www.dns-shop.ru/catalog/17a8a69116404e77/myshi/?stock=now-today-tomorrow-later&price=999-18499&f[579]=1q34&f[558]=1poc-96axb')
            dns_shops.check_changes(
                'https://www.dns-shop.ru/catalog/17a89a3916404e77/operativnaya-pamyat-dimm/?stock=now-today-tomorrow-later&f[z0mm]=1jdava&f[z1h1]=1jdavq&f[ms]=2ba')
        except Exception as ex:
            logging.error('ЕБУЧАЯ ОШИБКА DNS', ex)
            send_message('Парсер для DNS-SHOP упал. Если ошибка повторится обратитесь к администратору')

        try:
            rbt.check_changes()
        except Exception as ex:
            logging.error('ЕБУЧАЯ ОШИБКА RBT', ex)
            send_message('Парсер для RBT упал. Если ошибка повторится обратитесь к администратору')

        time.sleep(600)  # проверка изменений каждый 10 минут


if __name__ == '__main__':
    monitoring()
    # rbt.check_changes()
