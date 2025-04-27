import logging
from datetime import datetime, timedelta
from typing import Any

import pandas as pd
from pandas.io import json

from src.utils import currency_rates, get_price_stock, top_five_transaction

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


data_frame = pd.read_excel(
    r"C:\Users\YOGA 260\Pycharm_MY_Projects\Курсовые\project1\data\operations.xlsx"
)
# "../data/operations.xlsx""
df = data_frame


def main(date: str, df_transactions: Any, stocks: list, currency: list):
    """Функция создающая JSON ответ для главной страницы"""
    logger.info("Начало работы главной функции (main)")
    final_list = filter_by_date(date, df_transactions)
    greeting = greetings(f"{date} 00:00:00")
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
        date_obj = datetime(year, month, day)
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
            payment_date_obj = datetime.strptime(str(payment_date), "%d.%m.%Y")
        except ValueError:
            logger.warning(f"Неверный формат даты платежа: {payment_date}")
            continue

        if date_obj >= payment_date_obj >= date_obj - timedelta(days=day - 1):
            list_by_date.append(i)
    logger.info("Конец работы функции (filter_by_date)")
    return list_by_date


def for_each_card(my_list: list) -> list:
    """Функция создания информации по каждой карте"""
    logger.info("Начало работы функции (for_each_card)")
    cards = {}
    result = []
    logger.info("Перебор транзакций")
    for i in my_list:
        if i["Номер карты"] == "nan" or type(i["Номер карты"]) is float:
            continue
        elif i["Сумма платежа"] == "nan":
            continue
        else:
            if i["Номер карты"][1:] in cards:
                cards[i["Номер карты"][1:]] += float(str(i["Сумма платежа"])[1:])
            else:
                cards[i["Номер карты"][1:]] = float(str(i["Сумма платежа"])[1:])
    for k, v in cards.items():
        result.append(
            {
                "last_digits": k,
                "total_spent": round(v, 2),
                "cashback": round(v / 100, 2),
            }
        )
    logger.info("Завершение работы функции (for_each_card)")
    return result
