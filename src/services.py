import logging

from src.decorators import decorator_search

logger = logging.getLogger("services.log")
file_handler = logging.FileHandler("services.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


@decorator_search
def simple_search(df, query):
    # Если запрос пустой, возвращаем пустой массив
    if not query:
        return "[]"

    filtered_df = df[
        df.apply(lambda row: query.lower() in row.to_string().lower(), axis=1)
    ]

    return filtered_df.to_json(orient="records", force_ascii=False)
