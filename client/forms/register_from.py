import customtkinter
import customtkinter as ctk

from tkinter import StringVar
from tkinter.messagebox import showerror, showinfo
import client.forms.login_form

from client.api_requests.funcs import api_register


LOGIN_FONT = ("Arial", 16, "bold")


class RegisterForm(ctk.CTkToplevel):
    def __init__(self, parent) -> None:
        super().__init__()
        WIDTH = self.winfo_screenwidth()
        HEIGHT = self.winfo_screenheight()
        WIDTH = WIDTH // 2
        HEIGHT = HEIGHT // 2
        WIDTH = WIDTH - 200
        HEIGHT = HEIGHT - 200
        self.geometry(f'450x400+{WIDTH}+{HEIGHT}')

        self.parent = parent

        self.resizable(False, False)

        self.title("PCBoost")

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.fio_text = StringVar()
        self.login_text = StringVar()
        self.password_text = StringVar()

        self.draw_widgets()

    def draw_widgets(self):
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="PSBoost",
            font=("Arial", 32, "bold")
        )
        title_label.pack(ipady=10)
        # Login
        login_label = ctk.CTkLabel(
            self,
            text="Регистрация",
            font=("Arial", 18, "bold")
        )
        login_label.pack(ipady=5)

        login_row = ctk.CTkFrame(self)

        fio_inner_label = ctk.CTkLabel(
            login_row,
            text="ФИО",
            font=LOGIN_FONT
        )
        fio_inner_label.grid(row=0, column=0, pady=10)
        fio_inner_entry = ctk.CTkEntry(
            login_row,
            textvariable=self.fio_text,
            width=200
        )
        fio_inner_entry.grid(row=0, column=1, pady=10)
        login_inner_label = ctk.CTkLabel(
            login_row,
            text="Логин",
            font=LOGIN_FONT
        )
        login_inner_label.grid(row=1, column=0, pady=10)
        password_inner_label = ctk.CTkLabel(
            login_row,
            text="Пароль",
            font=LOGIN_FONT
        )
        password_inner_label.grid(row=2, column=0, padx=15, pady=10)
        login_inner_entry = ctk.CTkEntry(
            login_row,
            textvariable=self.login_text,
            width=200
        )
        login_inner_entry.grid(row=1, column=1, padx=15)
        password_inner_entry = ctk.CTkEntry(
            login_row,
            textvariable=self.password_text,
            show="*",
            width=200
        )
        password_inner_entry.grid(row=2, column=1)

        login_row.pack()

        footer_label = ctk.CTkLabel(
            self,
            text_color="#ADD8E6",
            text="Если у вас есть аккаунт - авторизируйтесь!",
            font=("Arial", 13, "underline")
        )
        footer_label.bind("<Button-1>", command=self.switch_login)
        footer_label.pack(pady=10)

        enter_button = ctk.CTkButton(
            self,
            width=200,
            command=self.register_command,
            text="Зарегистрироваться",
            font=LOGIN_FONT
        )
        enter_button.pack(pady=15)

    def register_command(self):
        fio = self.fio_text.get()
        login = self.login_text.get()
        password = self.password_text.get()

        response = api_register(
            fio=fio,
            username=login,
            password=password
        )

        if response["status"] == "ok":
            showinfo(title="Ok", message=response["message"])
            log_form = login_from.LoginForm(self.parent)
            self.withdraw()
            log_form.deiconify()
        else:
            showerror(title="Error", message=response["message"])

    def switch_login(self, *args):
        log_form = login_form.LoginForm(self.parent)
        self.withdraw()
        log_form.deiconify()

    def run_app(self) -> None:
        self.mainloop()