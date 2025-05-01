import json
import os
from unittest.mock import patch

import pandas as pd
from dotenv import load_dotenv

from src.utils import read_excel
from src.views import for_each_card, greetings, main

load_dotenv()
API_KEY_CUR = os.getenv("API_KEY_CUR")
my_list = read_excel("../data/operations.xlsx")
empty_list = []


def test_greetings():
    """Тестирование функции приветствия"""
    assert greetings("2023-10-05 09:30:00") == "Доброе утро"


def test_for_each_card():
    """Тестирование функции создающей информацию по каждой карте, в обычном режиме"""
    assert for_each_card(my_list) == [
        {"last_digits": "7197", "total_spent": 2504514.54, "cashback": 25045.15},
        {"last_digits": "5091", "total_spent": 18216.84, "cashback": 182.17},
        {"last_digits": "4556", "total_spent": 2103029.17, "cashback": 21030.29},
        {"last_digits": "1112", "total_spent": 46207.08, "cashback": 462.07},
        {"last_digits": "5507", "total_spent": 84000.0, "cashback": 840.0},
        {"last_digits": "6002", "total_spent": 69200.0, "cashback": 692.0},
        {"last_digits": "5441", "total_spent": 470854.8, "cashback": 4708.55},
    ]


def test_for_each_card_emp_att():
    """Тестирование функции создающей информацию по каждой карте, с пустым списком"""
    assert for_each_card(empty_list) == []


@patch("requests.get")
def test_main(mock_get):
    mock_get.return_value.json.return_value = {
        "greeting": "Добрый день",
        "cards": [
            {"last_digits": "4556", "total_spent": 30862.13, "cashback": 308.62},
            {"last_digits": "7197", "total_spent": 26890.62, "cashback": 268.91},
            {"last_digits": "5091", "total_spent": 1974.17, "cashback": 19.74},
        ],
        "top_transactions": [
            {
                "date": "25.11.2021",
                "amount": 4451.0,
                "category": "Другое",
                "description": "Федеральная Налоговая Служба",
            },
            {
                "date": "23.11.2021",
                "amount": 126105.03,
                "category": "Переводы",
                "description": "Перевод Кредитная карта. ТП 10.2 RUR",
            },
            {
                "date": "16.11.2021",
                "amount": 65.0,
                "category": "Бонусы",
                "description": "Вознаграждение за операции покупок",
            },
        ],
        "currency_rates": [
            {"currency": "USD", "rate": 91.38},
            {"currency": "EUR", "rate": 102.1},
        ],
        "stock_prices": [{"stock": "AAPL", "price": 228.03}],
    }
    res = main("2021.11.30", "../data/operations.xlsx", ["AAPL"], ["USD", "EUR"])
    ext = {
        "greeting": "Добрый день",
        "cards": [
            {"last_digits": "4556", "total_spent": 30862.13, "cashback": 308.62},
            {"last_digits": "7197", "total_spent": 26890.62, "cashback": 268.91},
            {"last_digits": "5091", "total_spent": 1974.17, "cashback": 19.74},
        ],
        "top_transactions": [
            {
                "date": "25.11.2021",
                "amount": 4451.0,
                "category": "Другое",
                "description": "Федеральная Налоговая Служба",
            },
            {
                "date": "23.11.2021",
                "amount": 126105.03,
                "category": "Переводы",
                "description": "Перевод Кредитная карта. ТП 10.2 RUR",
            },
            {
                "date": "16.11.2021",
                "amount": 65.0,
                "category": "Бонусы",
                "description": "Вознаграждение за операции покупок",
            },
        ],
        "currency_rates": [
            {"currency": "USD", "rate": 96.4},
            {"currency": "EUR", "rate": 105.85},
        ],
        "stock_prices": [{"stock": "AAPL", "price": 228.03}],
    }

    assert res == ext


def test_main_function_empty_input(mocker):
    """Тест с пустыми входными данными"""
    # Пустой DataFrame
    empty_df = pd.DataFrame()

    # Мокаем зависимости
    mocker.patch("your_module.filter_by_date", return_value=empty_df)
    mocker.patch("your_module.greetings", return_value="Привет")
    mocker.patch("your_module.for_each_card", return_value=[])
    mocker.patch("your_module.top_five_transaction", return_value=[])
    mocker.patch("your_module.get_price_stock", return_value={})
    mocker.patch("your_module.currency_rates", return_value={})
    mocker.patch("your_module.logger.info")

    # Вызываем функцию
    result_json = main("2023-05-01", empty_df, [], [])

    # Преобразуем JSON
    result = json.loads(result_json)

    # Проверяем базовую структуру
    assert len(result) == 1
