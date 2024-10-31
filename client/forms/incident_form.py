import customtkinter
import customtkinter as ctk

from client.api_requests.funcs import get_services_by_service_line

FONT_BOLD = ("Segoe UI", 14, "bold")
FONT = ("Segoe UI", 14)


class IncidentForm(ctk.CTkToplevel):
    def __init__(self, parent, token, incident) -> None:
        super().__init__()
        WIDTH = self.winfo_screenwidth()
        HEIGHT = self.winfo_screenheight()
        WIDTH = WIDTH // 2
        HEIGHT = HEIGHT // 2
        WIDTH = WIDTH - 200
        HEIGHT = HEIGHT - 200
        self.geometry(f'1000x700+{WIDTH}+{HEIGHT}')

        self.parent = parent
        self.token = token
        self.incident = incident

        self.resizable(False, False)

        self.title("PCBoost")

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.draw_widgets()
        self.grab_focus()

    def draw_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=1, fill="both")

        row_header = ctk.CTkFrame(main_frame)
        row_header.pack(expand=1, fill="both", anchor="n")

        incident_id_label = ctk.CTkLabel(
            row_header,
            text="ID: ",
            justify="left",
            anchor="w",
            font=FONT_BOLD
        )
        incident_id_label_text = ctk.CTkLabel(
            row_header,
            font=FONT,
            justify="left",
            anchor="w",
            width=200,
            text=self.incident["data"]["id"]
        )
        incident_id_label.grid(row=0, column=0, sticky="w", padx=8, pady=8)
        incident_id_label_text.grid(row=0, column=1, sticky="w", padx=8, pady=8)

        incident_date_label = ctk.CTkLabel(
            row_header,
            text="Дата: ",
            justify="left",
            anchor="w",
            font=FONT_BOLD
        )
        incident_date_label_text = ctk.CTkLabel(
            row_header,
            font=FONT,
            justify="left",
            anchor="w",
            width=200,
            text=self.incident["data"]["created_at"].split(".")[0].replace("T", " ")[:-3],
        )
        incident_date_label.grid(row=1, column=0, sticky="w", padx=8, pady=8)
        incident_date_label_text.grid(row=1, column=1, sticky="w", padx=8, pady=8)

        incident_topic_label = ctk.CTkLabel(
            row_header,
            text="Тема: ",
            justify="left",
            anchor="w",
            font=FONT_BOLD
        )
        incident_topic_label_text = ctk.CTkLabel(
            row_header,
            font=FONT,
            justify="left",
            anchor="w",
            width=200,
            text=self.incident["data"]["name"]
        )
        incident_topic_label.grid(row=2, column=0, sticky="w", padx=8, pady=8)
        incident_topic_label_text.grid(row=2, column=1, sticky="w", padx=8, pady=8)

        service_line_label = ctk.CTkLabel(
            row_header,
            text="Линия услуг: ",
            justify="left",
            anchor="w",
            font=FONT_BOLD
        )
        service_line_label_text = ctk.CTkLabel(
            row_header,
            font=FONT,
            justify="left",
            anchor="w",
            width=200,
            text=self.incident["data"]["service_line"]["name"]
        )
        service_line_label.grid(row=3, column=0, sticky="w", padx=8, pady=8)
        service_line_label_text.grid(row=3, column=1, sticky="w", padx=8, pady=8)

        desc_label = ctk.CTkLabel(
            row_header,
            text="Описание: ",
            justify="left",
            anchor="w",
            font=FONT_BOLD
        )
        desc_label_text = ctk.CTkLabel(
            row_header,
            font=FONT,
            justify="left",
            anchor="w",
            width=400,
            text=self.incident["data"]["description"]
        )
        desc_label.grid(row=4, column=0, sticky="w", padx=8, pady=8)
        desc_label_text.grid(row=4, column=1, sticky="w", padx=8, pady=8)

        status_label = ctk.CTkLabel(
            row_header,
            text="Статус: ",
            justify="left",
            anchor="w",
            font=FONT_BOLD
        )
        status_label_text = ctk.CTkLabel(
            row_header,
            font=FONT,
            justify="left",
            anchor="w",
            width=200,
            text=self.incident["data"]["status"]["name"]
        )
        status_label.grid(row=5, column=0, sticky="w", padx=8, pady=8)
        status_label_text.grid(row=5, column=1, sticky="w", padx=8, pady=8)

        user_label = ctk.CTkLabel(
            row_header,
            text="Сотрудник: ",
            justify="left",
            anchor="w",
            font=FONT_BOLD
        )

        if self.incident["data"]["user"] is not None:
            user_label_text = ctk.CTkLabel(
                row_header,
                font=FONT,
                justify="left",
                anchor="w",
                width=300,
                text=self.incident["data"]["user"]["username"] + " " + f'({self.incident["data"]["user"]["fio"]})'
            )
            user_label.grid(row=6, column=0, sticky="w", padx=8, pady=8)
            user_label_text.grid(row=6, column=1, sticky="w", padx=8, pady=8)

        if self.incident["data"]["from_client_fio"] is not None:
            client_label = ctk.CTkLabel(
                row_header,
                text="Клиент: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            client_label_text = ctk.CTkLabel(
                row_header,
                font=FONT,
                justify="left",
                anchor="w",
                width=300,
                text=self.incident["data"]["from_client_fio"]
            )
            client_label.grid(row=7, column=0, sticky="w", padx=8, pady=8)
            client_label_text.grid(row=7, column=1, sticky="w", padx=8, pady=8)

        if self.incident["data"]["solver"] is not None:
            solver_label = ctk.CTkLabel(
                row_header,
                text="Ответственный: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            solver_label_text = ctk.CTkLabel(
                row_header,
                font=FONT,
                justify="left",
                anchor="w",
                text=f'{self.incident["data"]["solver"]["username"]} ({self.incident["data"]["solver"]["fio"]})'
            )
            solver_label.grid(row=8, column=0, sticky="w", padx=8, pady=8)
            solver_label_text.grid(row=8, column=1, sticky="w", padx=8, pady=8)

        services = get_services_by_service_line(self.incident["data"]["service_line"]["name"])
        conf_text = ""
        for service in services["data"]["services"]:
            for line in service["description"].split(";"):
                conf_text += f"{line}\n"

        conf_label = ctk.CTkLabel(
            row_header,
            text="Связвнные ИТ-услуги: ",
            justify="left",
            anchor="w",
            font=FONT_BOLD
        )
        conf_label_text = ctk.CTkLabel(
            row_header,
            font=FONT,
            justify="left",
            anchor="w",
            text=conf_text
        )
        conf_label.grid(row=9, column=0, sticky="w", padx=8, pady=8)
        conf_label_text.grid(row=9, column=1, sticky="w", padx=8, pady=8)

    def grab_focus(self) -> None:
        self.grab_set()
        self.parent.wait_window(self)

    def run_app(self) -> None:
        self.mainloop()


