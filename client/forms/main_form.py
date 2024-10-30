import tkinter
from tkinter import ttk

import customtkinter
import customtkinter as ctk

from client.forms import login_form
from client.forms import create_incident_form
from client.forms import dialog_form
from client.forms import edit_incident_form
from client.forms import incident_form
from client.forms import service_form
from client.forms import edit_service_form
from client.forms import create_service_form

from tkinter.messagebox import showerror, showinfo

from client.api_requests.funcs import post_is_admin, post_is_tech
from client.api_requests.funcs import get_services, get_service, post_delete_service
from client.api_requests.funcs import get_incident, post_incidents_admin, post_incidents
from client.api_requests.users.users import get_users


FONT_BOLD = ("Segoe UI", 10, "bold")


class MainForm(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.token = None
        self.style = ttk.Style()
        self.tab_control = None

        WIDTH = self.winfo_screenwidth()
        HEIGHT = self.winfo_screenheight()
        WIDTH = WIDTH // 2
        HEIGHT = HEIGHT // 2
        WIDTH = WIDTH - 200
        HEIGHT = HEIGHT - 200
        self.geometry(f'1200x700+{WIDTH}+{HEIGHT}')

        self.resizable(False, False)

        self.title("PCBoost")

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        login = login_form.LoginForm(parent=self)
        self.withdraw()
        login.deiconify()

    def set_style(self):
        self.style.theme_use("default")
        self.style.configure(
            "Treeview.Heading",
            background="grey20",
            foreground="white",
            font=('Segoe UI', 12)
        )
        self.style.configure(
            "Treeview",
            fieldbackground="grey20",
            foreground="white",
            background="transparent",
        )
        self.style.map(
            "Treeview",
            background=[("selected", "disabled", "grey"), ("selected", "white")],
            foreground=[("selected", "disabled", "black"), ("selected", "black")]

        )
        self.style.configure('Treeview', rowheight=40)
        self.style.theme_use("default")
        self.style.configure(
            "TNotebook",
            background="grey20",
            tabposition="n"
        )
        self.style.configure(
            "TNotebook.Tab",
            background="dodgerblue1",
            foreground="white",
            font=('Arial', 14, "bold"),
            padding=[78, 10]
        )
        self.style.map(
            "TNotebook",
            background=[("selected", "blue")]
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", "white")],
            foreground=[("selected", "black")]
        )

    def draw_widgets(self):
        # Setting styles
        self.set_style()
        # Tabs Settings
        if self.tab_control is not None:
            self.tab_control.destroy()

        self.tab_control = ttk.Notebook(self)

        tab_services_buss = ctk.CTkFrame(self.tab_control)
        tab_services_tech = ctk.CTkFrame(self.tab_control)
        tab_incidents = ctk.CTkFrame(self.tab_control)
        tab_messenger = ctk.CTkFrame(self.tab_control)

        self.tab_control.add(tab_services_buss, text="Бизнес услуги")
        self.tab_control.add(tab_services_tech, text="Технические услуги")
        self.tab_control.add(tab_incidents, text="Инциденты")
        self.tab_control.add(tab_messenger, text="Мессенджер")

        self.tab_control.pack(expand=1, fill="both")

        services_data = get_services()

        i = 0
        if services_data["status"] == "ok":
            x_scroll = ttk.Scrollbar(tab_services_buss)
            x_scroll.pack(fill="y", side="right")

            columns = ('id', 'Линия услуг', 'Название')

            self.table = ttk.Treeview(tab_services_buss, xscrollcommand=x_scroll, columns=columns, show="headings")

            for col in columns:
                self.table.column(col, anchor="center")
                self.table.heading(col, text=col)

            for serv in services_data["data"]:
                if serv["service_type"]["name"] == "Бизнес услуги":
                    self.table.insert(
                        parent='',
                        index='end',
                        iid=i,
                        text='',
                        values=(serv["id"],
                                serv["service_line"]["name"],
                                serv["name"]
                                )
                    )
                    i += 1
            self.table.pack(fill=tkinter.BOTH, expand=1)

            footer_row = ctk.CTkFrame(tab_services_buss)
            footer_row.pack(fill="both")

            open_button = ctk.CTkButton(
                footer_row,
                text="Открыть",
                command=self.open_service_buss
            )
            open_button.grid(row=0, column=0, padx=8, pady=5)

            refresh_button = ctk.CTkButton(
                footer_row,
                text="Обновить",
                command=self.draw_widgets
            )
            refresh_button.grid(row=0, column=1, padx=8, pady=5)

            create_button = ctk.CTkButton(
                footer_row,
                text="Создать",
                command=self.create_service_buss
            )
            create_button.grid(row=0, column=2, padx=8, pady=5)

            edit_button = ctk.CTkButton(
                footer_row,
                text="Изменить",
                command=self.edit_service_buss
            )
            edit_button.grid(row=0, column=3, padx=8, pady=5)

            delete_button = ctk.CTkButton(
                footer_row,
                text="Удалить",
                command=self.delete_service_buss
            )
            delete_button.grid(row=0, column=4, padx=8, pady=5)

            # Tab tech services
            x1_scroll = ttk.Scrollbar(tab_services_tech)
            x1_scroll.pack(fill="y", side="right")

            columns1 = ('id', 'Линия услуг', 'Название')

            self.table1 = ttk.Treeview(tab_services_tech, xscrollcommand=x1_scroll, columns=columns, show="headings")

            for col in columns1:
                self.table1.column(col, anchor="center")
                self.table1.heading(col, text=col)

            for serv in services_data["data"]:
                if serv["service_type"]["name"] == "Технические услуги":
                    self.table1.insert(
                        parent='',
                        index='end',
                        iid=i,
                        text='',
                        values=(
                            serv["id"],
                            serv["service_line"]["name"],
                            serv["name"]
                        )
                    )
                    i += 1
            self.table1.pack(fill=tkinter.BOTH, expand=1)

            footer_row1 = ctk.CTkFrame(tab_services_tech)
            footer_row1.pack(fill="both")

            open_button1 = ctk.CTkButton(
                footer_row1,
                text="Открыть",
                command=self.open_service_tech
            )
            open_button1.grid(row=0, column=0, padx=8, pady=5)

            refresh_button1 = ctk.CTkButton(
                footer_row1,
                text="Обновить",
                command=self.draw_widgets
            )
            refresh_button1.grid(row=0, column=1, padx=8, pady=5)

            create_button1 = ctk.CTkButton(
                footer_row1,
                text="Создать",
                command=self.create_service_tech
            )
            create_button1.grid(row=0, column=2, padx=8, pady=5)

            edit_button1 = ctk.CTkButton(
                footer_row1,
                text="Изменить",
                command=self.edit_service_tech
            )
            edit_button1.grid(row=0, column=3, padx=8, pady=5)

            delete_button1 = ctk.CTkButton(
                footer_row1,
                text="Удалить",
                command=self.delete_service_tech
            )
            delete_button1.grid(row=0, column=4, padx=8, pady=5)
        else:
            error_label = ctk.CTkLabel(
                tab_services_buss,
                text=services_data["message"]
            )
            error_label.pack()
            error1_label = ctk.CTkLabel(
                tab_services_tech,
                text=services_data["message"]
            )
            error1_label.pack()

        # Tab Incidents
        incidents_user_data = post_incidents(self.token)
        incidents_admin_data = post_incidents_admin(self.token)

        footer_row2 = ctk.CTkFrame(tab_incidents)

        i = 0
        if incidents_admin_data["status"] == "ok" or incidents_user_data["status"] == "ok":
            x_scroll2 = ttk.Scrollbar(tab_incidents)
            x_scroll2.pack(fill="y", side="right")

            columns = ('id', 'Тема', 'Статус', 'Сотрудник', 'Услуга')

            self.table2 = ttk.Treeview(tab_incidents, xscrollcommand=x_scroll2, columns=columns, show="headings")

            for col in columns:
                self.table2.column(col, anchor="center")
                self.table2.heading(col, text=col)

            if post_is_admin(self.token)["data"] or post_is_tech(self.token)["data"]:
                for inc in incidents_admin_data["data"]:
                    if inc["user"] is None:
                        inc["user"] = {
                            "username": ""
                        }

                    self.table2.insert(
                        parent='',
                        index='end',
                        iid=i,
                        text='',
                        values=(inc["id"],
                                inc["name"],
                                inc["status"]["name"],
                                inc["user"]["username"],
                                inc["service_line"]["name"]
                                )
                    )

                    i += 1

                self.table2.pack(fill=tkinter.BOTH, expand=1)

                edit_button2 = ctk.CTkButton(
                    footer_row2,
                    text="Изменить",
                    command=self.edit_incident
                )
                edit_button2.grid(row=0, column=3, padx=8, pady=5)
            else:
                for inc in incidents_user_data["data"]:
                    self.table2.insert(
                        parent='',
                        index='end',
                        iid=i,
                        text='',
                        values=(inc["id"],
                                inc["name"],
                                inc["status"]["name"],
                                inc["user"]["username"],
                                inc["service_line"]["name"]
                                )
                    )
                    i += 1

                self.table2.pack(fill=tkinter.BOTH, expand=1)

            open_button2 = ctk.CTkButton(
                footer_row2,
                text="Открыть",
                command=self.open_incident
            )
            open_button2.grid(row=0, column=0, padx=8, pady=5)

            refresh_button2 = ctk.CTkButton(
                footer_row2,
                text="Обновить",
                command=self.draw_widgets
            )
            refresh_button2.grid(row=0, column=1, padx=8, pady=5)

            create_button2 = ctk.CTkButton(
                footer_row2,
                text="Создать",
                command=self.create_incident
            )
            create_button2.grid(row=0, column=2, padx=8, pady=5)

            footer_row2.pack(fill="both")

        footer_row3 = ctk.CTkFrame(tab_messenger)
        x_scroll3 = ttk.Scrollbar(tab_messenger)
        x_scroll3.pack(fill="y", side="right")

        columns = ('id', 'Username', 'ФИО')

        self.table3 = ttk.Treeview(tab_messenger, xscrollcommand=x_scroll3, columns=columns, show="headings")

        for col in columns:
            self.table3.column(col, anchor="center")
            self.table3.heading(col, text=col)

        i = 0
        for user in get_users()["data"]:
            self.table3.insert(
                parent='',
                index='end',
                iid=i,
                text='',
                values=(user["id"],
                        user["username"],
                        user["fio"]
                        )
            )
            i += 1

        self.table3.pack(fill=tkinter.BOTH, expand=1)

        open_button3 = ctk.CTkButton(
            footer_row3,
            text="Открыть",
            command=self.open_chat
        )
        open_button3.grid(row=0, column=0, padx=8, pady=5)

        footer_row3.pack(fill="both")

    def create_service_buss(self):
        create_service_form.CreateServiceForm(parent=self, token=self.token, type="Бизнес услуги")

    def open_service_buss(self):
        try:
            current_item = self.table.focus()
            service_id = int(self.table.item(current_item)["values"][0])
            service = get_service(service_id=service_id)
            service_form.ServiceForm(parent=self, service=service)
        except IndexError:
            showerror("Ошибка", "Выберите из таблицы!")

    def edit_service_buss(self):
        try:
            current_item = self.table.focus()
            service_id = int(self.table.item(current_item)["values"][0])
            edit_service_form.EditServiceForm(parent=self, token=self.token, service_id=service_id)
        except IndexError:
            showerror("Ошибка", "Выберите из таблицы!")

    def delete_service_buss(self):
        try:
            current_item = self.table.focus()
            service_id = int(self.table.item(current_item)["values"][0])
            check = post_delete_service(token=self.token, service_id=service_id)
            if check["status"] == "ok":
                showinfo(title=check["status"], message=check["message"])
            else:
                showerror(title=check["status"], message=check["message"])
        except IndexError:
            showerror("Ошибка", "Выберите из таблицы!")

    def create_service_tech(self):
        create_service_form.CreateServiceForm(parent=self, token=self.token, type="Технические услуги")

    def delete_service_tech(self):
        try:
            current_item = self.table1.focus()
            service_id = int(self.table1.item(current_item)["values"][0])
            check = post_delete_service(token=self.token, service_id=service_id)
            if check["status"] == "ok":
                showinfo(title=check["status"], message=check["message"])
            else:
                showerror(title=check["status"], message=check["message"])
        except IndexError:
            showerror("Ошибка", "Выберите из таблицы!")

    def open_service_tech(self):
        try:
            current_item = self.table1.focus()
            service_id = int(self.table1.item(current_item)["values"][0])
            service = get_service(service_id=service_id)
            service_form.ServiceForm(parent=self, service=service)
        except IndexError:
            showerror("Ошибка", "Выберите из таблицы!")

    def edit_service_tech(self):
        try:
            current_item = self.table1.focus()
            service_id = int(self.table1.item(current_item)["values"][0])
            edit_service_form.EditServiceForm(parent=self, token=self.token, service_id=service_id)
        except IndexError:
            showerror("Ошибка", "Выберите из таблицы!")

    def create_incident(self):
        create_incident_form.CreateIncidentForm(parent=self, token=self.token)

    def open_incident(self):
        try:
            current_item = self.table2.focus()
            incident_id = int(self.table2.item(current_item)["values"][0])
            incident = get_incident(incident_id=incident_id)
            incident_form.IncidentForm(token=self.token, parent=self, incident=incident)
        except IndexError:
            showerror("Ошибка", "Выберите из таблицы!")

    def edit_incident(self):
        try:
            current_item = self.table2.focus()
            incident_id = int(self.table2.item(current_item)["values"][0])
            incident = get_incident(incident_id=incident_id)
            edit_incident_form.EditIncidentForm(parent=self, token=self.token, incident=incident)
        except IndexError:
            showerror("Ошибка", "Выберите из таблицы!")

    def open_chat(self):
        try:
            current_item = self.table3.focus()
            recipient_username = str(self.table3.item(current_item)["values"][1])
            dialog_form.DialogForm(parent=self, token=self.token, recipient_username=recipient_username)
        except IndexError:
            showerror("Ошибка", "Выберите из таблицы!")

    def run_app(self) -> None:
        self.mainloop()
