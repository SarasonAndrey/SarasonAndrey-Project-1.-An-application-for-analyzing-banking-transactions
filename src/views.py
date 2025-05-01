import logging
import sys
from datetime import datetime
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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("date_filter.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


def greetings(input_datetime_str=None):
    """Функция для генерации приветствия в зависимости от времени"""
    if input_datetime_str is None:
        input_datetime = datetime.now()
    else:
        input_datetime = datetime.strptime(input_datetime_str, "%Y-%m-%d %H:%M:%S")

    if 6 <= input_datetime.hour < 12:
        return "Доброе утро"
    elif 12 <= input_datetime.hour < 18:
        return "Добрый день"
    elif 18 <= input_datetime.hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


data_frame = pd.read_excel(
    r"C:\Users\YOGA 260\Pycharm_MY_Projects\Курсовые\project1\data\operations.xlsx"
)

df = data_frame


def main_(date: str, df_transactions: Any, stocks: list, currency: list):
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


def filter_by_date(date: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Фильтрует DataFrame по диапазону дат за последнюю неделю

    Args:
        date (str): Дата в формате YYYY-MM-DD
        df (pd.DataFrame): Исходный DataFrame

    Returns:
        pd.DataFrame: Отфильтрованный DataFrame
    """
    try:
        # Проверка входных данных
        if df.empty:
            logger.warning("Входной DataFrame пуст")
            return pd.DataFrame()

        if not date:
            logger.warning("Дата не указана")
            return pd.DataFrame()

        # Преобразование входной даты
        target_date = pd.to_datetime(date)
        start_date = target_date - pd.Timedelta(days=6)
        end_date = target_date

        logger.info(f"Диапазон дат: {start_date.date()} - {end_date.date()}")

        # Преобразование столбца дат с учетом текущего формата
        df["Дата операции"] = pd.to_datetime(
            df["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
        )

        # Фильтрация
        filtered_df = df[
            (df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)
        ]

        # Логирование результатов
        logger.info(f"Найдено записей: {len(filtered_df)}")

        return filtered_df

    except Exception as e:
        logger.error(f"Ошибка при фильтрации: {e}")
        return pd.DataFrame()


def for_each_card(final_list):
    """
    Обработка транзакций по каждой карте

    Args:
        final_list (list or pd.DataFrame): Список или DataFrame транзакций

    Returns:
        list: Обработанные транзакции
    """
    logger.info("Начало работы функции (for_each_card)")
    logger.info("Перебор транзакций")

    # Преобразование DataFrame в list словарей, если это необходимо
    if isinstance(final_list, pd.DataFrame):
        final_list = final_list.to_dict("records")

    cards = []

    for i in final_list:
        try:
            # Проверка на NaN или пустое значение
            card_number = str(i.get("Номер карты", ""))

            if pd.isna(card_number) or card_number == "nan" or card_number == "":
                logger.warning(f"Пропуск транзакции с некорректным номером карты: {i}")
                continue

            # Дополнительная обработка транзакции
            # Здесь может быть ваша логика

            cards.append(i)

        except Exception as e:
            logger.error(f"Ошибка при обработке транзакции: {e}")
            logger.error(f"Проблемная транзакция: {i}")

    logger.info(f"Обработано транзакций: {len(cards)}")
    return cards



def main(date, df, stocks, currency):
    logger.info("Начало работы главной функции (main)")

    # Фильтрация по дате
    final_list = filter_by_date(date, df)

    # Преобразование в list словарей
    final_list = final_list.to_dict("records")

    # Вызов функции с обработкой
    try:
        cards = for_each_card(final_list)
        return cards
    except Exception as e:
        logger.error(f"Ошибка в функции main: {e}")
        return []
