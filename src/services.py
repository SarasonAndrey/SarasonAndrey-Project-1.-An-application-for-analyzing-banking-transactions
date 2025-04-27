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
def simple_search(df: pd.DataFrame, string_search: str):
    """Функция поиска по переданной строке"""
    result = []
    logger.info("Начало работы функции (simple_search)")

    # Преобразуем DataFrame в список словарей
    data_list = df.to_dict("records")

    for i in data_list:
        if string_search == "":
            return result

        # Обработка NaN значений
        description = str(i.get("Описание", "")).lower()
        category = str(i.get("Категория", "")).lower()
        search_term = string_search.lower()

        if search_term in description or search_term in category:
            result.append(i)

    logger.info("Конец работы функции (simple_search)")
    data_json = json.dumps(
        result,
        indent=4,
        ensure_ascii=False,
    )

    return data_json
