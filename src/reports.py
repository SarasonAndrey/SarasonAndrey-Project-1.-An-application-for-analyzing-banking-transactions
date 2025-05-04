import logging
from datetime import timedelta
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
):
    """
    Функция возвращающая траты за последние 3 месяца по заданной категории.

    Args:
        transactions (pd.DataFrame): DataFrame с транзакциями.
        category (str): Категория трат.
        date (Optional[str]): Дата для фильтрации (формат "DD-MM-YYYY").

    Returns:
        List[float]: Список сумм трат за указанный период.
    """
    logger.info("Начало работы")

    # Проверка наличия необходимых столбцов
    required_columns = {"Категория", "Дата платежа", "Сумма платежа"}
    if not required_columns.issubset(transactions.columns):
        logger.error(
            f"Отсутствуют необходимые столбцы: {required_columns - set(transactions.columns)}"
        )
        return []

    # Преобразование даты в формат datetime
    transactions["Дата платежа"] = pd.to_datetime(
        transactions["Дата платежа"], format="%d.%m.%Y", errors="coerce"
    )

    # Фильтрация по категории
    filtered = transactions[transactions["Категория"] == category]

    # Определение временного диапазона
    if date is None:
        logger.info("Обработка условия на отсутствие даты")
        date_start = pd.Timestamp.now() - timedelta(days=90)
    else:
        logger.info("Обработка условия на создание даты")
        try:
            day, month, year = map(int, date.split("-"))
            date_obj = pd.Timestamp(year=year, month=month, day=day)
            date_start = date_obj - timedelta(days=90)
        except ValueError as e:
            logger.error(f"Ошибка при обработке даты: {e}")
            return []

    # Фильтрация по временному диапазону
    filtered = filtered[
        (filtered["Дата платежа"] >= date_start)
        & (filtered["Дата платежа"] <= date_start + timedelta(days=90))
    ]

    # Возврат списка сумм платежей
    result = filtered["Сумма платежа"].dropna().tolist()
    logger.info("Завершение работы функции")
    return result
