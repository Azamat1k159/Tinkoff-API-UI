import threading
import tkinter
import customtkinter as ck
import Main
import asyncio

n = "\n"


def error_empty_token():
    error_window = ck.CTk()
    label = ck.CTkLabel(error_window, text="Ошибка токена")
    label.grid(row=0)
    button = ck.CTkButton(error_window, text="Закрыть", command=error_window.destroy)
    button.grid(row=1)
    error_window.mainloop()


class UI:

    def __init__(self):
        self.Token = Main.txt_file_read()
        self.window = ck.CTk()

    def window_init(self, w: int, h: int):
        self.window.title("Tinkoff-Invest")
        self.window.geometry(f'{w}x{h}')
        t1 = threading.Thread(target=self.window.mainloop())
        t1.start()

    def add_buttons(self):
        self.frame_login = ck.CTkFrame(
            self.window,
        )
        self.frame_login.place(relx=0.50, rely=0.30, anchor=tkinter.CENTER)

        token_label = ck.CTkLabel(
            self.frame_login,
            text="Введите токен от аккаунта",
        )
        token_label.grid(row=0, column=0, padx=15, pady=30)

        self.token_entry = ck.CTkEntry(
            self.frame_login,
        )
        self.token_entry.grid(row=0, column=1, padx=15, pady=10)

        again_button = ck.CTkButton(
            self.frame_login,
            text='Тот же токен',
            command=lambda: self.on_login(Main.check_token(self.Token)),
        )
        again_button.grid(row=1, column=0, padx=15, pady=10)

        login_button = ck.CTkButton(
            self.frame_login,
            text='Войти',
            command=lambda: self.on_login(False),
        )
        login_button.grid(row=1, column=1, padx=15, pady=10)

        close_button = ck.CTkButton(
            self.frame_login,
            text="Закрыть окно",
            command=self.window.destroy,
            fg_color="#db4848",
            hover_color="#bf3636"
        )
        close_button.grid(row=2, column=0, padx=15, pady=10)

        setting_button = ck.CTkButton(
            self.frame_login,
            text="Настройки",
            command=self.setting_window
        )
        setting_button.grid(row=2, column=1, padx=15, pady=10)

    async def add_buttons_main(self):
        frame_main = ck.CTkFrame(
            self.window,
        )
        frame_main.place(relx=0.5, rely=0.70, anchor=tkinter.CENTER)

        refresh_button = ck.CTkButton(
            frame_main,
            text="Обновить"
        )
        refresh_button.grid(row=0, column=1, padx=15, pady=15)

        buy_button = ck.CTkButton(
            frame_main,
            text="Купить",
        )
        buy_button.grid(row=0, column=0, padx=15, pady=15)

        close_button = ck.CTkButton(
            frame_main,
            text="Закрыть окно",
            fg_color="#db4848",
            hover_color="#bf3636",
            command=self.window.destroy,
        )
        close_button.grid(row=1, column=0, padx=15, pady=15)

        req_button = ck.CTkButton(
            frame_main,
            text="Заявки",
        )
        req_button.grid(row=1, column=1, padx=15, pady=15)

        button_back = ck.CTkButton(
            frame_main,
            text="Назад",
            command=lambda: self.back_event(frame_main, tab_frame)
        )
        button_back.grid(row=2, column=0, padx=20, pady=(10, 20))

        tab_frame = ck.CTkFrame(
            self.window,
            corner_radius=0,
            border_width=0,
            fg_color=("gray95", "gray10")
        )
        tab_frame.place(relx=0.5, rely=0.35, anchor=tkinter.CENTER)

        self.tabview = ck.CTkTabview(tab_frame)
        self.tabview.grid(row=0, column=0, padx=50, pady=25)
        self.tabview.add("Баланс")
        label_balance = ck.CTkLabel(self.tabview.tab("Баланс"),
                                    text=f"{Main.balance(self.Token)} \n Тикеты: \n "
                                         f"{''.join(x + n for x in Main.all_figi(self.Token))}")

        label_balance.pack(padx=15, pady=15)
        t2 = threading.Thread(target=Main.tabs_add, args=(self.tabview, Main.count_tabs(self.Token)[0], Main.count_tabs(self.Token)[1], self.Token))
        t2.start()

    def setting_window(self):
        self.frame_login.destroy()
        settings_frame = ck.CTkFrame(
            self.window,
        )
        settings_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


        button_back = ck.CTkButton(
            settings_frame,
            text="Назад",
            command=lambda: self.back_event(settings_frame, False)
        )
        button_back.grid(row=2, column=0, padx=20, pady=(10, 20))



    def back_event(self, frame, frame_s):
        frame.destroy()
        if frame_s:
            frame_s.destroy()
        self.add_buttons()

    def on_login(self, connect: bool):
        if connect:
            self.frame_login.destroy()
            asyncio.run(self.add_buttons_main())
        if not connect:
            if self.token_entry.get():
                Main.txt_file_write(self.Token)
                self.on_login(Main.check_token(self.token_entry.get()))
            elif not Main.check_token(Main.txt_file_read()):
                error_empty_token()
            else:
                self.on_login(True)
