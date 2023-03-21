"""
Tinkoff-bot
"""
import time
import customtkinter as ck
from tinkoff.invest import Client, PortfolioResponse
import ui


def cast_money(money) -> float:
    return money.units + money.nano / 1e9


ck.set_appearance_mode("System")
ck.set_default_color_theme("dark-blue.json")


def hash_add(token, num, hash_tab: ck.CTkTabview):
    with Client(token) as client:
        r: PortfolioResponse = client.operations.get_portfolio(account_id=account_id_func(token))
        for i in range(num):
            hash_tab.update({r.positions[i].figi: cast_money(r.positions[i].average_position_price)})
    return hash_tab


def tinka(token: str, num: int) -> str:
    with Client(token) as client:
        r: PortfolioResponse = client.operations.get_portfolio(account_id=account_id_func(token))
        return str(
            f"""Тикет: {str(r.positions[num].figi)}\n Кол-во {str(r.positions[num].quantity.units)}
            \n Цена за шт: {str(cast_money(r.positions[num].current_price))}
            \n Стоимость всех: {str(round(cast_money(r.positions[num].current_price)
                                          * cast_money(r.positions[num].quantity), 2))}""")


def txt_file_read():
    with open("TOKEN.txt", "r", encoding='utf-8') as f:
        return f.readline()


def txt_file_write(token: str):
    with open("TOKEN.txt", "r", encoding='utf-8') as f:
        f.write(token)


def count_tabs(token: str):
    with Client(token) as client:
        r: PortfolioResponse = client.operations.get_portfolio(account_id=account_id_func(token))
        return len(r.positions), [r.positions[i].figi for i in range(len(r.positions))]


def balance(token):
    with Client(token) as client:
        r: PortfolioResponse = client.operations.get_portfolio(account_id=account_id_func(token))
        return "Баланс: {0}".format(
            str(round(cast_money(r.total_amount_bonds) + cast_money(r.total_amount_currencies), 2)))


def all_figi(token):
    with Client(token) as client:
        r: PortfolioResponse = client.operations.get_portfolio(account_id=account_id_func(token))
        return [r.positions[i].figi for i in range(len(r.positions))]


def price_now(token, num):
    with Client(token) as client:
        r: PortfolioResponse = client.operations.get_portfolio(account_id=account_id_func(token))
        return cast_money(r.positions[num].current_price)


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


def tabs_add(tabview, x, data, token, hash_tmp):
    if not hash_tmp:
        hash_tmp = hash_add(token, x, {})
    for i in range(x):
        try:
            tabview.add(f"{data[i]}")
            label = ck.CTkLabel(tabview.tab(f"{data[i]}"), text=tinka(token, i), justify="left")
            label.pack(padx=20, pady=20)
            button_buy = ck.CTkButton(tabview.tab(f"{data[i]}"), text="Купить")
            button_sell = ck.CTkButton(tabview.tab(f"{data[i]}"), text="Продать")
            button_buy.pack(padx=30, pady=15)
            button_sell.pack(padx=30, pady=15)
        except:
            if hash_tmp[f"{data[i]}"] <= price_now(token, i) and "RUB" not in data[i]:
                param = "₽ ➕"
            elif "RUB" not in data[i]:
                param = "₽ ➖"
            else:
                param = "₽"
            tabview.tab(f"{data[i]}").children["!ctklabel"].configure(text=tinka(token, i) + f"{param}")

    time.sleep(2)
    tabs_add(tabview, x, data, token, hash_tmp)


if __name__ == '__main__':
    win = ui.UI()
    win.add_buttons()
    win.window_init(750, 750)
