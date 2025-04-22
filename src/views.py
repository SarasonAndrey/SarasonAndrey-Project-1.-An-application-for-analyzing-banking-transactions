import datetime
import logging

logger = logging.getLogger("views.log")
file_handler = logging.FileHandler("views.log", "a")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def filter_by_date(date: str, my_list: list) -> list:
    """Функция фильтрующая данные по заданной дате"""
    list_by_date = []
    logger.info("Начало работы функции (filter_by_date)")
    if date == "":
        return list_by_date
    try:
        year, month, day = int(date[0:4]), int(date[5:7]), int(date[8:10])
        date_obj = datetime.datetime(year, month, day)
    except (ValueError, IndexError):
        logger.error("Неверный формат даты")
        return list_by_date

    for i in my_list:
        if not isinstance(i, dict):
            logger.warning("Элемент списка не является словарем")
            continue

        payment_date = i.get("Дата платежа")
        if payment_date == "nan" or isinstance(payment_date, float):
            continue

        try:
            payment_date_obj = datetime.datetime.strptime(str(payment_date), "%d.%m.%Y")
        except ValueError:
            logger.warning(f"Неверный формат даты платежа: {payment_date}")
            continue

        if date_obj >= payment_date_obj >= date_obj - datetime.timedelta(days=day - 1):
            list_by_date.append(i)
    logger.info("Конец работы функции (filter_by_date)")
    return list_by_date
