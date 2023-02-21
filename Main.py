from tinkoff.invest import Client
import tkinter
import customtkinter as ck

ck.set_appearance_mode("System")
ck.set_default_color_theme("dark-blue.json")


def txt_file():
    f = open("TOKEN.txt", "r")
    return f.readline()


def account_id_func(token_invest: str) -> str:
    with Client(token_invest) as client:
        return client.users.get_accounts().accounts[0].id


def check_token(token: str) -> bool:
    try:
        with Client(token) as client:
            if client.operations.get_portfolio(account_id=account_id_func(txt_file())):
                return True
    except:
        return False


class UI:

    def __init__(self):
        self.token_entry = None
        self.Token = txt_file()
        self.window = ck.CTk()

    def window_init(self, w: int, h: int):
        self.window.title("Tinkoff-Invest")
        self.window.geometry(f'{w}x{h}')
        self.window.mainloop()

    def add_buttons(self):
        frame_login = ck.CTkFrame(
            self.window,
            width=200,
            height=200,
        )
        frame_login.place(relx=0.50, rely=0.30, anchor=tkinter.CENTER)

        token_label = ck.CTkLabel(
            frame_login,
            text="Введите токен от аккаунта",
        )
        token_label.grid(row=0, column=0, padx=15, pady=30)

        self.token_entry = ck.CTkEntry(
            frame_login,
        )
        self.token_entry.grid(row=0, column=1, padx=15, pady=10)

        again_button = ck.CTkButton(
            frame_login,
            text='Тот же токен',
            command=lambda: self.on_login(check_token(self.Token)),
        )
        again_button.grid(row=1, column=0, padx=15, pady=10)

        login_button = ck.CTkButton(
            frame_login,
            text='Войти',
            command=lambda: self.on_login(False),
        )
        login_button.grid(row=1, column=1, padx=15, pady=10)

        close_button = ck.CTkButton(
            frame_login,
            text="Закрыть окно",
            command=lambda: self.window.destroy(),
            fg_color="#db4848",
            hover_color="#bf3636"
        )
        close_button.grid(row=2, column=0, padx=15, pady=10)

        setting_button = ck.CTkButton(
            frame_login,
            text="Настройки",
        )
        setting_button.grid(row=2, column=1, padx=15, pady=10)

    def add_buttons_main(self):
        frame_main = ck.CTkFrame(
            self.window,
            width=150,
            height=150,
        )
        frame_main.place(relx=0.5, rely=0.70, anchor=tkinter.CENTER)

        token_label = ck.CTkLabel(
            self.window,
            text="111",
        )
        token_label.place(relx=0.50, rely=0.20, anchor=tkinter.CENTER)

        refresh_button = ck.CTkButton(
            frame_main,
            text="Обновить",
        )
        refresh_button.grid(row=0, column=1, padx=15, pady=15)

        close_button = ck.CTkButton(
            frame_main,
            text="Закрыть окно",
            command=lambda: self.window.destroy(),
        )
        close_button.grid(row=0, column=0, padx=15, pady=15)

    def new_window(self):
        self.window.destroy()
        self.window = ck.CTk()
        self.add_buttons_main()
        self.window_init(500, 500)

    def on_login(self, connect: bool):
        if connect:
            self.new_window()
        if not connect:
            if self.token_entry.get():
                self.on_login(check_token(self.token_entry.get()))
            elif not check_token(txt_file()):
                print("error")
            else:
                self.on_login(True)


if __name__ == '__main__':
    win = UI()
    win.add_buttons()
    win.window_init(500, 500)
