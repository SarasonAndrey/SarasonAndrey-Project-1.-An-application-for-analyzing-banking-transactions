import json
import logging

import pandas as pd

from src.decorators import decorator_search

logger = logging.getLogger("services.log")
file_handler = logging.FileHandler("services.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


@decorator_search
def simple_search(df, string_search):
    # Преобразуем DataFrame в более простой формат

    # Шаг 1: Преобразование Timestamp в строки
    df = df.copy()
    df['Дата операции'] = df['Дата операции'].astype(str)

    # Шаг 2: Поиск по строке (регистронезависимый)
    result = df[
        df.apply(
            lambda row: string_search.lower() in str(row).lower(),
            axis=1
        )
    ]

    try:
        # Преобразование в список словарей и сериализация в JSON
        result_list = result.to_dict('records')

        # Используем ensure_ascii=False для корректной поддержки кириллицы
        data_json = json.dumps(result_list, ensure_ascii=False)

        return data_json

    except Exception as e:
        # Простая обработка ошибок
        print(f"Ошибка при поиске: {e}")
        return "[]"
