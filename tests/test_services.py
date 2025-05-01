import json

import pandas as pd

from src.services import simple_search


def test_simple_search_empty_string():
    """Тест на пустую строку поиска"""
    df = pd.DataFrame(
        [
            {"Описание": "Тестовая запись", "Категория": "Тест"},
            {"Описание": "Другая запись", "Категория": "Пример"},
        ]
    )
    result = simple_search(df, "")
    assert result == "[]"


def test_simple_search_match_description():
    """Тест на поиск по описанию"""
    df = pd.DataFrame(
        [
            {"Описание": "Мобильный телефон", "Категория": "Электроника"},
            {"Описание": "Планшет", "Категория": "Компьютеры"},
        ]
    )
    result = json.loads(simple_search(df, "мобильный"))
    assert len(result) == 1
    assert result[0]["Описание"] == "Мобильный телефон"


def test_simple_search_match_category():
    """Тест на поиск по категории"""
    df = pd.DataFrame(
        [
            {"Описание": "MacBook", "Категория": "Компьютеры"},
            {"Описание": "iPhone", "Категория": "Телефоны"},
        ]
    )
    result = json.loads(simple_search(df, "телефоны"))
    assert len(result) == 1
    assert result[0]["Категория"] == "Телефоны"


def test_simple_search_case_insensitive():
    """Тест на регистронезависимый поиск"""
    df = pd.DataFrame(
        [
            {"Описание": "SAMSUNG", "Категория": "Электроника"},
            {"Описание": "Apple", "Категория": "Техника"},
        ]
    )
    result = json.loads(simple_search(df, "samsung"))
    assert len(result) == 1
    assert result[0]["Описание"] == "SAMSUNG"


def test_simple_search_no_matches():
    """Тест на отсутствие совпадений"""
    df = pd.DataFrame(
        [
            {"Описание": "Ноутбук", "Категория": "Компьютеры"},
            {"Описание": "Планшет", "Категория": "Техника"},
        ]
    )
    result = json.loads(simple_search(df, "смартфон"))
    assert result == []
