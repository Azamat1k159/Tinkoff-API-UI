import threading
import tkinter
import customtkinter as ck
import main
import asyncio

n = "\n"
def error_empty_token():
    error_window = ck.CTk()
    label = ck.CTkLabel(error_window, text="Ошибка токена")
    label.grid(row=0)
    button = ck.CTkButton(error_window, text="Закрыть", command=error_window.destroy)
    button.grid(row=1)
    error_window.mainloop()

class UI_elements():
    def create_button(self, Frame, Text: str, row: int, column: int, Command = None):
        create_button = ck.CTkButton(
            Frame,
            text=Text,
            command=Command
        )
        create_button.grid(row=row, column=column, padx=15, pady=10)
        return create_button

    def create_frame(self, master, relx, rely, anchor):
        frmame = ck.CTkFrame(
            master,
        )
        frmame.place(relx=relx, rely=rely, anchor=anchor)
        return frmame
class UI(UI_elements):

    def __init__(self):
        self.tabview = None
        self.token_entry = None
        self.frame_login = None
        self.token = main.txt_file_read()
        self.window = ck.CTk()

    def window_init(self, w: int, h: int):
        self.window.title("Tinkoff-Invest")
        self.window.geometry(f'{w}x{h}')
        thread1 = threading.Thread(target=self.window.mainloop())
        thread1.start()

    def add_buttons(self):
        self.frame_login = UI_elements.create_frame(self, self.window, 0.50, 0.30, tkinter.CENTER)

        token_label = ck.CTkLabel(
            self.frame_login,
            text="Введите токен от аккаунта",
        )
        token_label.grid(row=0, column=0, padx=15, pady=30)

        self.token_entry = ck.CTkEntry(
            self.frame_login,
        )
        self.token_entry.grid(row=0, column=1, padx=15, pady=10)

        again_button = UI_elements.create_button(self, self.frame_login, 'Тот же токен', 1, 0, Command=lambda: self.on_login(main.check_token(self.token)))

        login_button = UI_elements.create_button(self, self.frame_login, 'Войти', 1, 1, Command=lambda: self.on_login(False))

        close_button = ck.CTkButton(
            self.frame_login,
            text="Закрыть окно",
            command=lambda: exit(),
            fg_color="#db4848",
            hover_color="#bf3636"
        )
        close_button.grid(row=2, column=0, padx=15, pady=10)

        setting_button = UI_elements.create_button(self, self.frame_login, 'Настройки', 2, 1, Command=lambda: self.setting_window())
    async def add_buttons_main(self):
        self.frame_main = UI_elements.create_frame(self, self.window, relx=0.5, rely=0.70, anchor=tkinter.CENTER)

        frame_main = self.frame_main

        refresh_button = UI_elements.create_button(self, frame_main, 'Обновить', 0, 1)

        buy_button = UI_elements.create_button(self, frame_main, 'Купить', 0, 0)

        close_button = ck.CTkButton(
            frame_main,
            text="Закрыть окно",
            fg_color="#db4848",
            hover_color="#bf3636",
            command=lambda: exit(),
        )
        close_button.grid(row=1, column=0, padx=15, pady=15)

        req_button = UI_elements.create_button(self, frame_main, 'Заявки', 1, 1)

        setting_button = UI_elements.create_button(self, frame_main, 'Настройки', 2, 1, Command=self.setting_window)

        button_back = UI_elements.create_button(self, frame_main, 'Назад', 2, 0, Command=lambda: self.back_event(frame_main, tab_frame))

        tab_frame = ck.CTkFrame(
            self.window,
            corner_radius=0,
            border_width=0,
            fg_color=("gray95", "gray10")
        )
        tab_frame.place(relx=0.5, rely=0.30, anchor=tkinter.CENTER)

        self.tabview = ck.CTkTabview(tab_frame)
        self.tabview.grid(row=0, column=0, padx=50, pady=25)
        self.tabview.add("Баланс")
        label_balance = ck.CTkLabel(self.tabview.tab("Баланс"),
                                    text=f"{main.balance(self.token)} \n Тикеты: \n "
                                         f"{''.join(x + n for x in main.all_figi(self.token))}")

        label_balance.pack(padx=15, pady=15)
        thread2 = threading.Thread(target=main.tabs_add, args=(self.tabview, main.count_tabs(self.token)[0],
                                                               main.count_tabs(self.token)[1], self.token, None))
        thread2.start()


    def setting_window(self):
        self.frame_login.destroy()

        settings_frame= UI_elements.create_frame(self, self.window, relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        button_back = UI_elements.create_button(self, settings_frame, 'Назад', 2, 0, Command=lambda: self.back_event(settings_frame, False))

    def back_event(self, frame: ck.CTkFrame, frame_s: ck.CTkFrame):
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
                self.token = self.token_entry.get()
                main.txt_file_write(self.token)
                self.on_login(main.check_token(self.token_entry.get()))
            elif not main.check_token(main.txt_file_read()):
                error_empty_token()
            else:
                self.on_login(True)
