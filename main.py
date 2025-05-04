from pprint import pprint

from src.reports import spending_by_category
from src.services import simple_search
from src.utils import currency_rates, get_price_stock, read_excel, top_five_transaction
from src.views import df, filter_by_date, for_each_card, greetings, main, main_

date = "2021-12-12"
string_search = "Ozon.ru"
currency = ["USD", "EUR", "RUB"]
stocks = ["AAPL", "GOOGL", "MSFT"]
category = "Переводы"
df_transactions = df

if __name__ == "__main__":
    print("#" * 20, "\n")
    print(greetings("2023-10-05 09:30:00"))
    print("#" * 20, "\n")
    print(df[["Дата платежа", "Сумма операции"]].head())
    print("#" * 20, "\n")
    print(main(date, df, stocks, currency))
    print("#" * 20, "\n")
    print(filter_by_date(date, df))
    print("#" * 20, "\n")
    pprint(simple_search(df, string_search))
    print("#" * 20, "\n")
    pprint(read_excel(df.head(3)))
    print("#" * 20, "\n")
    pprint(for_each_card(df.to_dict("records")))
    print("#" * 20, "\n")
    print(currency_rates(currency))
    print("#" * 20, "\n")
    pprint(top_five_transaction(df.to_dict("records")))
    print("#" * 20, "\n")
    print(get_price_stock(stocks))
    print("#" * 20, "\n")
    print(spending_by_category(df, category, date))
    print("#" * 20, "\n")
    print(main_(date, df_transactions, stocks, currency))
