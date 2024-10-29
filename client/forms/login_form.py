import customtkinter
import customtkinter as ctk

from tkinter import StringVar
from tkinter.messagebox import showerror

from client.forms import register_from

from client.api_requests.funcs import api_login


LOGIN_FONT = ("Arial", 16, "bold")


class LoginForm(ctk.CTkToplevel):
    def __init__(self, parent) -> None:
        super().__init__()
        WIDTH = self.winfo_screenwidth()
        HEIGHT = self.winfo_screenheight()
        WIDTH = WIDTH // 2
        HEIGHT = HEIGHT // 2
        WIDTH = WIDTH - 200
        HEIGHT = HEIGHT - 200
        self.geometry(f'450x400+{WIDTH}+{HEIGHT}')
        self.resizable(False, False)

        self.parent = parent

        self.title("PCBoost")

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.login_text = StringVar()
        self.password_text = StringVar()

        self.draw_widgets()

    def draw_widgets(self):
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="PCBoost",
            font=("Arial", 32, "bold")
        )
        title_label.pack(ipady=10)
        # Login
        login_label = ctk.CTkLabel(
            self,
            text="Вход",
            font=("Arial", 18, "bold")
        )
        login_label.pack(ipady=5)
        # Frame for fields
        login_row = ctk.CTkFrame(self)
        login_inner_label = ctk.CTkLabel(
            login_row,
            text="Логин",
            font=LOGIN_FONT
        )
        login_inner_label.grid(row=0, column=0, pady=10)
        password_inner_label = ctk.CTkLabel(
            login_row,
            text="Пароль",
            font=LOGIN_FONT
        )
        password_inner_label.grid(row=1, column=0, padx=15, pady=10)
        login_inner_entry = ctk.CTkEntry(
            login_row,
            textvariable=self.login_text,
            width=200
        )
        login_inner_entry.grid(row=0, column=1, padx=15)
        password_inner_entry = ctk.CTkEntry(
            login_row,
            textvariable=self.password_text,
            show="*",
            width=200
        )
        password_inner_entry.grid(row=1, column=1)

        login_row.pack()

        footer_label = ctk.CTkLabel(
            self,
            text_color="#ADD8E6",
            text="Если у вас нет аккаунта - зарегистрируйтесь!",
            font=("Arial", 13, "underline")
        )
        footer_label.bind("<Button-1>", command=self.switch_register)
        footer_label.pack(pady=10)

        enter_button = ctk.CTkButton(
            self,
            width=200,
            command=self.login_command,
            text="Войти",
            font=LOGIN_FONT
        )
        enter_button.pack(pady=15)

    def login_command(self):
        login = self.login_text.get()
        password = self.password_text.get()

        response = api_login(
            username=login,
            password=password
        )

        if response["status"] == "ok":
            self.parent.token = response["token"]
            self.parent.draw_widgets()
            self.withdraw()
            self.parent.deiconify()
        else:
            showerror(title="Ошибка", message=response["message"])

    def switch_register(self, *args):
        reg_form = register_from.RegisterForm(self.parent)
        self.withdraw()
        reg_form.deiconify()

    def run_app(self) -> None:
        self.mainloop()
