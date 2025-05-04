import os
from unittest.mock import Mock, patch

import pandas as pd
import pytest
from dotenv import load_dotenv

from src.utils import currency_rates, get_price_stock, read_excel, top_five_transaction
from src.views import df

load_dotenv()
API_KEY_CUR = os.getenv("API_KEY_CUR")
my_list = df
empty_list = []


def test_read_excel():
    # Создаем тестовые данные
    test_data = {
        "Дата платежа": ["2023-01-01", "2023-01-02"],
        "Статус": ["Completed", "Pending"],
        "Сумма платежа": [100.50, 200.75],
        "Валюта платежа": ["USD", "EUR"],
        "Категория": ["Продукты", "Транспорт"],
        "Описание": ["Покупка в магазине", "Такси"],
        "Номер карты": ["1234", "5678"],
    }

    # Создаем Excel-файл для теста
    df = pd.DataFrame(test_data)
    test_file = "test_payments.xlsx"
    df.to_excel(test_file, index=False)

    # Вызываем функцию
    result = read_excel(test_file)
    assert len(result) == 2, "Должно быть 2 записи"


@patch("requests.get")
def test_currency_rates(mock_get):
    """Тестирование функции вывода курса валют"""
    mock_response_usd = Mock()
    mock_response_usd.json.return_value = {"conversion_rates": {"RUB": 96.4}}
    mock_response_eur = Mock()
    mock_response_eur.json.return_value = {"conversion_rates": {"RUB": 105.85}}
    mock_get.side_effect = [mock_response_usd, mock_response_eur]
    result = currency_rates(["USD", "EUR"])
    expected = [{"currency": "USD", "rate": 96.4}, {"currency": "EUR", "rate": 105.85}]
    assert result == expected


@pytest.mark.parametrize(
    "input_data, expected_result",
    [
        # Тест 1: Нормальный список словарей с пополнениями
        (
            [
                {"Категория": "Пополнения", "Сумма": "100"},
                {"Категория": "Пополнения", "Сумма": "200"},
                {"Категория": "Пополнения", "Сумма": "50"},
                {"Категория": "Пополнения", "Сумма": "300"},
                {"Категория": "Пополнения", "Сумма": "150"},
                {"Категория": "Пополнения", "Сумма": "250"},
            ],
            [
                {"Категория": "Пополнения", "Сумма": "300"},
                {"Категория": "Пополнения", "Сумма": "250"},
                {"Категория": "Пополнения", "Сумма": "200"},
                {"Категория": "Пополнения", "Сумма": "150"},
                {"Категория": "Пополнения", "Сумма": "100"},
            ],
        ),
        ([], []),
        (
            [
                {"Категория": "Покупки", "Сумма": "100"},
                {"Категория": "Услуги", "Сумма": "200"},
            ],
            [],
        ),
        (
            pd.DataFrame(
                [
                    {"Категория": "Пополнения", "Сумма": "400"},
                    {"Категория": "Пополнения", "Сумма": "500"},
                    {"Категория": "Пополнения", "Сумма": "300"},
                ]
            ),
            [
                {"Категория": "Пополнения", "Сумма": "500"},
                {"Категория": "Пополнения", "Сумма": "400"},
                {"Категория": "Пополнения", "Сумма": "300"},
            ],
        ),
    ],
)
def test_top_five_transaction(input_data, expected_result):

    result = top_five_transaction(input_data)

    print(f"Длина результата: {len(result)}")
    assert len(result) == len(expected_result), "Неверное количество транзакций"

    for i in range(len(result)):
        print(f"Проверка транзакции {i + 1}")
        print(f"Ожидаемое значение: {expected_result[i]}")
        print(f"Фактическое значение: {result[i]}")

        # Проверяем каждое поле транзакции
        assert (
            result[i]["Категория"] == expected_result[i]["Категория"]
        ), "Неверная категория"
        assert result[i]["Сумма"] == expected_result[i]["Сумма"], "Неверная сумма"


@pytest.mark.parametrize(
    "input_data",
    [
        [
            {"Категория": "Пополнения", "Сумма": "abc"},
            {"Категория": "Пополнения", "Сумма": "100"},
        ],
        [
            {"Категория": "Пополнения", "Сумма": 100},
            {"Категория": "Пополнения", "Сумма": "200"},
        ],
    ],
)
def test_top_five_transaction_edge_cases(input_data):

    try:
        result = top_five_transaction(input_data)
        print("Результат для краевого случая:", result)
    except Exception as e:
        print(f"Перехвачено исключение: {e}")
        assert False, f"Функция вызвала неожиданное исключение: {e}"


def test_top_five_transaction_emp_att():
    """Тестирование функции для получения топ-5 транзакций по сумме платежа, с пустым списком"""
    assert top_five_transaction(empty_list) == []


@patch("requests.get")
def test_fetch_stock_prices(mock_get):
    """Тестирование функции получения данных об акциях из списка S&P500"""

    mock_get.return_value.json.return_value = {"Global Quote": {"05. price": 210.00}}

    list_stocks = ["AAPL"]

    result = get_price_stock(list_stocks)
    expected = [
        {"stock": "AAPL", "price": 210.00},
    ]
    assert result == expected
