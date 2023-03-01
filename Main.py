import customtkinter as ck
import time
from tinkoff.invest import Client, PortfolioResponse
import UI


def cast_money(x) -> float:
    return x.units + x.nano / 1e9


ck.set_appearance_mode("System")
ck.set_default_color_theme("dark-blue.json")


# noinspection PyTypeChecker
def tinka(token: str, num: int) -> str:
    with Client(token) as client:
        r: PortfolioResponse = client.operations.get_portfolio(account_id=account_id_func(token))
        dop = str("Тикет " + str(r.positions[num].figi) + "\n" + " Кол-во " + str(
            r.positions[num].quantity.units) + "\n" + " Цена за шт " + str(cast_money(r.positions[num].current_price)
                                                                           ) + "\n" + " Стоимость всех  " + "\n" + str(
            round(
                cast_money(r.positions[num].current_price) * cast_money(r.positions[num].quantity), 2)))
        return dop


def txt_file_read():
    f = open("TOKEN.txt", "r")
    return f.readline()

def txt_file_write(token):
    f = open("TOKEN.txt", "w")
    f.write(token)

def count_tabs(token: str):
    with Client(token) as client:
        r: PortfolioResponse = client.operations.get_portfolio(account_id=account_id_func(token))
        return len(r.positions), [r.positions[i].figi for i in range(len(r.positions))]


def balance(token):
    with Client(token) as client:
        r: PortfolioResponse = client.operations.get_portfolio(account_id=account_id_func(token))
        return "Баланс: " + str(round(cast_money(r.total_amount_bonds) + cast_money(r.total_amount_currencies), 2))


def all_figi(token):
    with Client(token) as client:
        r: PortfolioResponse = client.operations.get_portfolio(account_id=account_id_func(token))
        return [r.positions[i].figi for i in range(len(r.positions))]


def account_id_func(token_invest: str) -> str:
    if token_invest:
        with Client(token_invest) as client:
            return client.users.get_accounts().accounts[0].id


def check_token(token: str) -> bool:
    try:
        with Client(token) as client:
            if client.operations.get_portfolio(account_id=account_id_func(token)):
                return True
    except:
        return False


def tabs_add(tabview, x, data, token):
    for i in range(x):
        try:
            tabview.add(f"{data[i]}")
            label = ck.CTkLabel(tabview.tab(f"{data[i]}"), text=tinka(token, i))
            label.pack(padx=20, pady=20)
            button_buy = ck.CTkButton(tabview.tab(f"{data[i]}"), text="Купить")
            button_sell = ck.CTkButton(tabview.tab(f"{data[i]}"), text="Продать")
            button_buy.pack(padx=30, pady=15)
            button_sell.pack(padx=30, pady=15)
        except:
            tabview.tab(f"{data[i]}").children["!ctklabel"].configure(text=tinka(token, i))
    print(2)
    time.sleep(2)
    try:
        tabs_add(tabview, x, data, token)
    except:
        tabs_add(tabview, x, data, token)

# class Tinkoff(UI):
#     def buy(self):
#         ...
#
#     def sell(self):
#         ...
#
#     def search(self):
#         ...
#
#     def figi_to_ticket(self):
#         ...



if __name__ == '__main__':
    win = UI.UI()
    win.add_buttons()
    win.window_init(750, 750)

