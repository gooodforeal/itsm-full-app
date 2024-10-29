import customtkinter
import customtkinter as ctk

from tkinter import ttk
from tkinter.messagebox import showerror, showinfo

from tkinter import StringVar

from client.api_requests.funcs import post_edit_incident, get_statuses

FONT_BOLD = ("Segoe UI", 14, "bold")
FONT = ("Segoe UI", 14)


class EditIncidentForm(ctk.CTkToplevel):
    def __init__(self, parent, token, incident) -> None:
        super().__init__()
        WIDTH = self.winfo_screenwidth()
        HEIGHT = self.winfo_screenheight()
        WIDTH = WIDTH // 2
        HEIGHT = HEIGHT // 2
        WIDTH = WIDTH - 200
        HEIGHT = HEIGHT - 200
        self.geometry(f'1200x700+{WIDTH}+{HEIGHT}')

        self.parent = parent
        self.token = token
        self.incident = incident

        self.resizable(False, False)

        self.title("PCBoost")

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.status = StringVar()
        self.status.set(incident["data"]["status"]["name"])

        self.draw_widgets()
        self.grab_focus()

    def draw_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=1, fill="both")

        row_header = ctk.CTkFrame(main_frame)
        row_header.pack(expand=1, fill="both", anchor="n")

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
        incident_topic_label.grid(row=0, column=0, sticky="w", padx=8, pady=8)
        incident_topic_label_text.grid(row=0, column=1, sticky="w", padx=8, pady=8)

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
        service_line_label.grid(row=1, column=0, sticky="w", padx=8, pady=8)
        service_line_label_text.grid(row=1, column=1, sticky="w", padx=8, pady=8)

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
        desc_label.grid(row=2, column=0, sticky="w", padx=8, pady=8)
        desc_label_text.grid(row=2, column=1, sticky="w", padx=8, pady=8)

        status_label = ctk.CTkLabel(
            row_header,
            text="Статус: ",
            justify="left",
            anchor="w",
            font=FONT_BOLD
        )
        status_label_text = ctk.CTkComboBox(
            row_header,
            font=FONT,
            values=[status["name"] for status in get_statuses()["data"]],
            variable=self.status
        )
        status_label.grid(row=3, column=0, sticky="w", padx=8, pady=8)
        status_label_text.grid(row=3, column=1, sticky="w", padx=8, pady=8)

        if self.incident["data"]["user"] is not None:
            user_label = ctk.CTkLabel(
                row_header,
                text="Сотрудник: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            user_label_text = ctk.CTkLabel(
                row_header,
                font=FONT,
                justify="left",
                anchor="w",
                width=300,
                text=self.incident["data"]["user"]["username"] + " " + f'({self.incident["data"]["user"]["fio"]})'
            )
            user_label.grid(row=4, column=0, sticky="w", padx=8, pady=8)
            user_label_text.grid(row=4, column=1, sticky="w", padx=8, pady=8)

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
            client_label.grid(row=5, column=0, sticky="w", padx=8, pady=8)
            client_label_text.grid(row=5, column=1, sticky="w", padx=8, pady=8)

        # Footer
        footer_frame = ctk.CTkFrame(main_frame)
        footer_frame.pack(fill="both")

        create_btn = ctk.CTkButton(
            footer_frame,
            text="Ок",
            command=self.edit_incident
        )
        create_btn.grid(row=0, column=3, padx=8, pady=5)

    def edit_incident(self):
        response = post_edit_incident(
            token=self.token,
            status=self.status.get(),
            incident_id=self.incident["data"]["id"]
        )

        if response["status"] == "ok":
            showinfo(title="Ok", message=response["message"])
            self.parent.grab_set()
            self.withdraw()
            self.parent.deiconify()
        else:
            showerror(title="Error", message=response["message"])

    def grab_focus(self) -> None:
        self.grab_set()
        self.parent.wait_window(self)

    def run_app(self) -> None:
        self.mainloop()


