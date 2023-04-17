"""
Tinkoff-bot
"""
import time
import customtkinter as ck
from tinkoff.invest import Client, PortfolioResponse
import tinkoff
import ui


def cast_money(money: tinkoff.invest.MoneyValue) -> float:
    return money.units + money.nano / 1e9


ck.set_appearance_mode("System")
ck.set_default_color_theme("dark-blue.json")

def hash_add(token: str, num: int, hash_tab: dict):
    with Client(token) as client:
        request: PortfolioResponse = client.operations.get_portfolio(account_id=account_id_func(token))
        for i in range(num):
            hash_tab.update({str(request.positions[i].figi): cast_money(request.positions[i].average_position_price)})
    return hash_tab


def get_last_price(token: str, figi: str) -> float:
    with Client(token) as client:
        request: PortfolioResponse = client.market_data.get_last_prices(figi=[figi])
        return cast_money(request.last_prices[0].price)


def tinka(token: str, num: int) -> str:
    with Client(token) as client:
        request: PortfolioResponse = client.operations.get_portfolio(account_id=account_id_func(token))
        return str(
            f"""Тикет: {str(figi := request.positions[num].figi)}\n Кол-во {str(quantity := request.positions[num].quantity.units)}
            \n Цена за шт: {str(last_price := get_last_price(token, figi))}
            \n Стоимость всех: {str(round(last_price * cast_money(request.positions[num].quantity), 2))}""")


def txt_file_read():
    with open("TOKEN.txt", "r", encoding='utf-8') as f:
        return f.read()

def txt_file_write(token: str):
    with open("TOKEN.txt", "w", encoding='utf-8') as f:
        f.write(token)


def count_tabs(token: str):
    with Client(token) as client:
        request: PortfolioResponse = client.operations.get_portfolio(account_id=account_id_func(token))
        return len(request.positions), [request.positions[i].figi for i in range(len(request.positions))]


def balance(token: str):
    with Client(token) as client:
        request: PortfolioResponse = client.operations.get_portfolio(account_id=account_id_func(token))
        return "Баланс: {0}".format(
            str(round(cast_money(request.total_amount_bonds) + cast_money(request.total_amount_currencies), 2)))


def all_figi(token: str):
    with Client(token) as client:
        request: PortfolioResponse = client.operations.get_portfolio(account_id=account_id_func(token))
        return [request.positions[i].figi for i in range(len(request.positions))]


def price_now(token: str, num: int):
    with Client(token) as client:
        request: PortfolioResponse = client.operations.get_portfolio(account_id=account_id_func(token))
        return cast_money(request.positions[num].current_price)


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

def post_order_func(token: str, tiket_id: str, account_id: str, type_operation: int):
    with Client(token) as client:
        client.orders.post_order(figi=tiket_id, quantity=1, direction=type_operation, account_id=account_id, order_type=type_operation, order_id= '122212uyuioic')

def tabs_add(tabview: ck.CTkTabview, x: int, data: list, token: str, hash_tmp: dict):
    while True:
        if not hash_tmp:
            hash_tmp = hash_add(token, x, {})
        for i in range(x):
            try:
                tabview.add(f"{data[i]}")
                label = ck.CTkLabel(tabview.tab(f"{data[i]}"), text="Загрузка...", justify="left")
                label.pack(padx=20, pady=20)
                if data[i] != 'RUB000UTSTOM':
                    button_open = ck.CTkButton(tabview.tab(f"{data[i]}"), text="Открыть графики")
                    button_buy = ck.CTkButton(tabview.tab(f"{data[i]}"), text="Купить", command=lambda: post_order_func(token, data[i], account_id_func(token), 1))
                    button_sell = ck.CTkButton(tabview.tab(f"{data[i]}"), text="Продать", command=lambda: post_order_func(token, data[i], account_id_func(token), 2))
                    button_buy.pack(padx=30, pady=15)
                    button_sell.pack(padx=30, pady=15)
                    button_open.pack(padx=30, pady=15)

            except:
                if hash_tmp[f"{data[i]}"] <= price_now(token, i) and "RUB" not in data[i]:
                    param = "₽ ➕"
                elif "RUB" not in data[i]:
                    param = "₽ ➖"
                else:
                    param = "₽"
                tabview.tab(f"{data[i]}").children["!ctklabel"].configure(text=tinka(token, i) + f"{param}")
        time.sleep(2)


if __name__ == '__main__':
    win = ui.UI()
    win.add_buttons()
    win.window_init(750, 750)
