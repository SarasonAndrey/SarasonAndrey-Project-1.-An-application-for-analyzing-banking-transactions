import logging
from datetime import timedelta

import pandas as pd
import pytest

from src.views import filter_by_date, for_each_card, greetings, main

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Фикстуры для тестирования
@pytest.fixture
def sample_dataframe():
    """Создание тестового DataFrame"""
    return pd.DataFrame(
        {
            "Дата операции": [
                "01.12.2023 10:00:00",
                "02.12.2023 15:30:00",
                "05.12.2023 20:45:00",
            ],
            "Номер карты": ["1234", "5678", "9012"],
            "Сумма": [100, 200, 300],
        }
    )


@pytest.mark.parametrize(
    "time_str, expected",
    [
        ("2023-01-01 07:00:00", "Доброе утро"),
        ("2023-01-01 13:00:00", "Добрый день"),
        ("2023-01-01 19:00:00", "Добрый вечер"),
        ("2023-01-01 03:00:00", "Доброй ночи"),
    ],
)
def test_greetings(time_str, expected):
    """Тест функции приветствия"""
    result = greetings(time_str)
    assert result == expected, f"Неверное приветствие для времени {time_str}"


def test_filter_by_date_normal_case(sample_dataframe):
    """Тест фильтрации по дате"""
    # Используем последнюю дату в DataFrame как опорную
    target_date = "2023-12-05"

    # Выполняем фильтрацию
    result = filter_by_date(target_date, sample_dataframe)

    # Проверки
    assert not result.empty, "Результат фильтрации не должен быть пустым"
    print(f"Найдено записей: {len(result)}")

    # Проверка диапазона дат
    result_dates = result["Дата операции"].dt.date
    min_date = pd.to_datetime(target_date) - timedelta(days=6)
    max_date = pd.to_datetime(target_date)

    assert all(
        min_date.date() <= date <= max_date.date() for date in result_dates
    ), "Найдены даты вне допустимого диапазона"


def test_filter_by_date_edge_cases():
    """Тест краевых случаев фильтрации"""
    # Пустой DataFrame
    empty_df = pd.DataFrame()
    result_empty = filter_by_date("2023-12-05", empty_df)
    assert result_empty.empty, "Должен возвращаться пустой DataFrame для пустого входа"

    # None дата
    result_none = filter_by_date(None, empty_df)
    assert result_none.empty, "Должен возвращаться пустой DataFrame для None даты"


def test_for_each_card_normal_case(sample_dataframe):
    """Тест обработки транзакций"""

    transactions = sample_dataframe.to_dict("records")

    result = for_each_card(transactions)

    assert len(result) == len(transactions), "Количество транзакций должно совпадать"

    for transaction in result:
        assert transaction.get("Номер карты"), "Номер карты не должен быть пустым"


def test_for_each_card_invalid_data():
    """Тест обработки некорректных данных"""

    invalid_transactions = [
        {"Номер карты": "", "Сумма": 100},
        {"Номер карты": None, "Сумма": 200},
        {"Номер карты": "nan", "Сумма": 300},
    ]

    result = for_each_card(invalid_transactions)

    for transaction in result:
        print(transaction)

    assert len(result) == 0, "Должны быть отфильтрованы все невалидные транзакции"


def test_for_each_card_mixed_data():
    """Тест обработки смешанных данных"""
    mixed_transactions = [
        {"Номер карты": "1234", "Сумма": 100},
        {"Номер карты": "", "Сумма": 200},
        {"Номер карты": "5678", "Сумма": 300},
        {"Номер карты": None, "Сумма": 400},
        {"Номер карты": "nan", "Сумма": 500},
    ]

    result = for_each_card(mixed_transactions)

    for transaction in result:
        print(transaction)

    assert len(result) == 2, "Должны быть отфильтрованы все невалидные транзакции"

    valid_card_numbers = {"1234", "5678"}
    for transaction in result:
        assert (
            transaction["Номер карты"] in valid_card_numbers
        ), "Найдена невалидная транзакция"


def test_main_integration(sample_dataframe):
    """Интеграционный тест основной функции"""
    # Параметры для теста
    test_date = "2023-12-05"
    test_stocks = ["AAPL", "GOOGL"]
    test_currency = ["USD", "EUR"]

    try:

        result = main(test_date, sample_dataframe, test_stocks, test_currency)

        assert isinstance(result, list), "Результат должен быть списком"

    except Exception as e:
        pytest.fail(f"Unexpectected error in main function: {e}")
