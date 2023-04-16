import shelve
import string

from config import basedir
import os
from typing import Optional, Tuple

filename = os.path.join(basedir, 'settings')


def get_delivery_cost() -> tuple:
    """
    Get delivery cost
    :return: (First 3 km, and longer)
    """
    settings = shelve.open(filename)
    if 'delivery_cost' not in settings:
        settings['delivery_cost'] = (3000, 1000)
    value = settings['delivery_cost']
    settings.close()
    return value


def set_delivery_cost(prices: tuple):
    """
    Set delivary prices
    :param prices: (First 3 km, and longer)
    :return: void
    """
    settings = shelve.open(filename)
    settings['delivery_cost'] = prices
    settings.close()


##############TIME##################

def get_timelimits() -> tuple:
    """
    Time limits
    :return: (start, end)
    """
    settings = shelve.open(filename)
    if 'timelimits' not in settings:
        settings['timelimits'] = ['08:00', '20:00']
    value = settings['timelimits']
    settings.close()
    return value



def set_timelimits(times: tuple):
    """

    """
    settings = shelve.open(filename)
    settings['timelimits'] = times
    settings.close()

###########NOTIFICATION############

def get_timenotify():
    """
    Time notification)
    """
    settings = shelve.open(filename)
    if 'timenotify' not in settings:
        settings['timenotify'] = ('Mы закрыты. Работаем с ...  до ...')
    value = settings['timenotify']
    settings.close()
    return value


def set_timenotify(notify):
    """

    """
    settings = shelve.open(filename)
    settings['timenotify'] = notify
    settings.close()
#########################


def get_cafe_coordinates() -> Optional[Tuple[float, float]]:
    """
    Cafe coordinates
    :return: (latitude, longitude)
    """
    settings = shelve.open(filename)
    if 'cafe_coordinates' not in settings:
        settings['cafe_coordinates'] = (41.2646500, 69.2162700)
    value = settings['cafe_coordinates']
    settings.close()
    return value


def set_cafe_coordinates(coordinates: tuple):
    """
    Set cafe coordinates
    :param coordinates: (latitude, longitude)
    :return: void
    """
    settings = shelve.open(filename)
    settings['cafe_coordinates'] = coordinates
    settings.close()


def set_limit_delivery_price(price: int):
    """
    Set limit delivery cost
    :param price: price value
    :return: void
    """
    settings = shelve.open(filename)
    settings['limit_delivery_price'] = price
    settings.close()


def get_limit_delivery_price() -> int:
    """
    Get limit delivery cost or set default value - 15000
    :return: limit delivery price
    """
    settings = shelve.open(filename)
    if 'limit_delivery_price' not in settings:
        settings['limit_delivery_price'] = 15000
    value = settings['limit_delivery_price']
    settings.close()
    return value


def set_currency_value(value: int):
    """
    Set currency value
    :param value: currency value
    :return: void
    """
    settings = shelve.open(filename)
    settings['currency_value'] = value
    settings.close()


def get_currency_value() -> int:
    """
    Get currency value
    :return: currency value
    """
    settings = shelve.open(filename)
    if 'currency_value' not in settings:
        settings['currency_value'] = 10200
    value = settings['currency_value']
    settings.close()
    return value
