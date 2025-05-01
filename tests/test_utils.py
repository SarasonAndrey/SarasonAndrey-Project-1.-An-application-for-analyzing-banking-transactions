import os
from unittest.mock import Mock, patch

from dotenv import load_dotenv

from src.utils import currency_rates, get_price_stock, read_excel, top_five_transaction
from src.views import for_each_card

load_dotenv()
API_KEY_CUR = os.getenv("API_KEY_CUR")
my_list = read_excel("../data/operations.xlsx")
empty_list = []


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


def test_top_five_transaction():
    """Тестирование функции для получения топ-5 транзакций по сумме платежа, в обычном режиме"""
    assert top_five_transaction(my_list) == [
        {
            "amount": 90044.51,
            "category": "Переводы",
            "date": "21.03.2019",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
        {
            "amount": 8626.0,
            "category": "Бонусы",
            "date": "20.05.2021",
            "description": "Компенсация покупки",
        },
        {
            "amount": 6100.0,
            "category": "Зарплата",
            "date": "30.04.2019",
            "description": 'Пополнение. ООО "ФОРТУНА". Зарплата',
        },
        {
            "amount": 6100.0,
            "category": "Зарплата",
            "date": "15.04.2019",
            "description": 'Пополнение. ООО "ФОРТУНА". Аванс',
        },
        {
            "amount": 721.38,
            "category": "Каршеринг",
            "date": "12.12.2021",
            "description": "Ситидрайв",
        },
    ]


def test_top_five_transaction_emp_att():
    """Тестирование функции для получения топ-5 транзакций по сумме платежа, с пустым списком"""
    assert top_five_transaction(empty_list) == []


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
