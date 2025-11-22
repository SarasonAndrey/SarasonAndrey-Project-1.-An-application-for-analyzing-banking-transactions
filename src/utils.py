import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

API_KEY_CUR = os.getenv("API_KEY_CUR")
SP_500_API_KEY = os.getenv("SP_500_API_KEY")

logger = logging.getLogger("utils.log")
file_handler = logging.FileHandler("utils.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
load_dotenv()


def read_excel(path_file: str) -> list[dict]:
    """Функция читает .xlsx файл и возвращает список словарей"""
    if isinstance(path_file, str):
        df = pd.read_excel(path_file)
        # Если уже DataFrame - возвращаем как есть
    elif isinstance(path_file, pd.DataFrame):
        df = path_file
    else:
        raise ValueError("Передайте путь к файлу или DataFrame")

    result = df.apply(
        lambda row: {
            "Дата платежа": row["Дата платежа"],
            "Статус": row["Статус"],
            "Сумма платежа": row["Сумма платежа"],
            "Валюта платежа": row["Валюта платежа"],
            "Категория": row["Категория"],
            "Описание": row["Описание"],
            "Номер карты": row["Номер карты"],
        },
        axis=1,
    ).tolist()
    return result


def currency_rates(currencies: list[str]) -> list[dict[str, str | float]]:
    """Функция запроса курса валют"""
    logger.info("Начало работы функции (currency_rates)")
    api_key = API_KEY_CUR
    url_base = "https://v6.exchangerate-api.com/v6/{}/latest/{}"
    result = []

    try:
        for curr in currencies:
            try:
                url = url_base.format(api_key, curr)
                response = requests.get(url, timeout=10)
                response.raise_for_status()  # Вызовет исключение при ошибках HTTP
                body_dict = response.json()

                rate = body_dict.get("conversion_rates", {}).get("RUB", 0)
                result.append({"currency": curr, "rate": round(rate, 2)})
            except requests.RequestException as e:
                logger.error(f"Ошибка при запросе курса для {curr}: {e}")
                result.append({"currency": curr, "rate": None})
    except Exception as e:
        logger.error(f"Непредвиденная ошибка: {e}")
        return []

    logger.info("Окончание работы функции - currency_rates")
    return result


def top_five_transaction(final_list):
    # Проверка, является ли входной объект DataFrame
    if isinstance(final_list, pd.DataFrame):
        # Преобразование DataFrame в список словарей
        transactions = final_list.to_dict("records")
    else:
        transactions = final_list

    # Проверка на пустоту
    if not transactions:
        return []

    # Фильтрация пополнений
    replenishments = [
        trans for trans in transactions if trans.get("Категория") == "Пополнения"
    ]

    # Сортировка и первые 5
    try:
        top_five = sorted(
            replenishments, key=lambda x: float(x.get("Сумма", 0)), reverse=True
        )[:5]
    except (ValueError, TypeError) as e:
        logger.error(f"Ошибка сортировки транзакций: {e}")
        top_five = []

    return top_five


def get_price_stock(stocks: list) -> list:
    """Функция для получения данных об акциях из списка S&P500"""
    logger.info("Начало работы функции (get_price_stock)")
    api_key = SP_500_API_KEY
    stock_prices = []

    for stock in stocks:
        try:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
            response = requests.get(url, timeout=5, allow_redirects=False)
            result = response.json()

            # Проверка структуры ответа
            if "Global Quote" in result and "05. price" in result["Global Quote"]:
                stock_prices.append(
                    {
                        "stock": stock,
                        "price": round(float(result["Global Quote"]["05. price"]), 2),
                    }
                )
            else:
                logger.warning(f"Неверный формат ответа для {stock}")
                stock_prices.append(
                    {
                        "stock": stock,
                        "price": None,
                    }
                )

        except requests.RequestException as e:
            logger.error(f"Ошибка сети для {stock}: {e}")
            stock_prices.append(
                {
                    "stock": stock,
                    "price": None,
                }
            )
        except (ValueError, KeyError) as e:
            logger.error(f"Ошибка обработки данных для {stock}: {e}")
            stock_prices.append(
                {
                    "stock": stock,
                    "price": None,
                }
            )

    logger.info("Функция get_price_stock завершила работу")
    return stock_prices
