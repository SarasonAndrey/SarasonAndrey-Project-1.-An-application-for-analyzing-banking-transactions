import datetime
import logging
from datetime import datetime
import os

import pandas as pd
from pandas.io import json

from src.utils import (
    currency_rates,
    for_each_card,
    get_price_stock,
    top_five_transaction,
)

logger = logging.getLogger("views.log")
file_handler = logging.FileHandler("views.log", "a")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

logger = logging.getLogger("utils.log")
file_handler = logging.FileHandler("main.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def greetings(input_datetime_str: str) -> str:
    """Функция приветствия"""

    input_datetime = datetime.strptime(input_datetime_str, "%Y-%m-%d %H:%M:%S")
    time_obj = input_datetime.hour

    if 5 <= time_obj < 12:
        return '"Доброе утро"'
    elif 12 <= time_obj < 18:
        return '"Добрый день"'
    elif 18 <= time_obj < 22:
        return '"Добрый вечер"'
    else:
        return '"Доброй ночи"'


# data_frame = pd.read_excel("../data/operations.xlsx")
base_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(base_dir, '..', 'data', 'operations.xlsx')



def main(date: str, df_transactions, stocks: list, currency: list):
    """Функция создающая JSON ответ для главной страницы"""
    logger.info("Начало работы главной функции (main)")
    final_list = filter_by_date(date, df_transactions)
    greeting = greetings()
    cards = for_each_card(final_list)
    top_trans = top_five_transaction(final_list)
    stocks_prices = get_price_stock(stocks)
    currency_r = currency_rates(currency)
    logger.info("Создание JSON ответа")
    result = [
        {
            "greeting": greeting,
            "cards": cards,
            "top_transactions": top_trans,
            "currency_rates": currency_r,
            "stock_prices": stocks_prices,
        }
    ]
    date_json = json.dumps(
        result,
        indent=4,
        ensure_ascii=False,
    )
    logger.info("Завершение работы главной функции (main)")
    return date_json


def filter_by_date(date: str, my_list: list) -> list:
    """Функция фильтрующая данные по заданной дате"""
    list_by_date = []
    logger.info("Начало работы функции (filter_by_date)")
    if date == "":
        return list_by_date
    try:
        year, month, day = int(date[0:4]), int(date[5:7]), int(date[8:10])
        date_obj = datetime.datetime(year, month, day)
    except (ValueError, IndexError):
        logger.error("Неверный формат даты")
        return list_by_date

    for i in my_list:
        if not isinstance(i, dict):
            logger.warning("Элемент списка не является словарем")
            continue

        payment_date = i.get("Дата платежа")
        if payment_date == "nan" or isinstance(payment_date, float):
            continue

        try:
            payment_date_obj = datetime.datetime.strptime(str(payment_date), "%d.%m.%Y")
        except ValueError:
            logger.warning(f"Неверный формат даты платежа: {payment_date}")
            continue

        if date_obj >= payment_date_obj >= date_obj - datetime.timedelta(days=day - 1):
            list_by_date.append(i)
    logger.info("Конец работы функции (filter_by_date)")
    return list_by_date
