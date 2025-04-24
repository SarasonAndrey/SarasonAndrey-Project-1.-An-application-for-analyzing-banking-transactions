from src.views import greetings, main
import pandas as pd


data_frame = pd.read_excel(r"C:\Users\YOGA 260\Pycharm_MY_Projects\Курсовые\project1\data\operations.xlsx")
if __name__ == "__main__":
    print(greetings("2023-10-05 09:30:00"))
    print('#' * 20)


    print(data_frame.head())

