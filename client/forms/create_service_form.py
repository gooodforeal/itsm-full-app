import customtkinter
import customtkinter as ctk

from tkinter import ttk
from tkinter.messagebox import showerror, showinfo

from tkinter import StringVar

from client.api_requests.funcs import get_service_lines, post_create_service

FONT_BOLD = ("Segoe UI", 14, "bold")
FONT = ("Segoe UI", 14)


class CreateServiceForm(ctk.CTkToplevel):
    def __init__(self, parent, token, type) -> None:
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
        self.type = type

        self.resizable(False, False)

        self.title("PCBoost")

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.service_line = StringVar()
        self.service_name = StringVar()
        self.service_description = StringVar()

        self.draw_widgets()
        self.grab_focus()

    def draw_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=1, fill="both")

        service_lines = get_service_lines()

        row_header = ctk.CTkFrame(main_frame)
        row_header.pack(expand=1, fill="both", anchor="n")

        service_type_label = ctk.CTkLabel(
            row_header,
            text="Тип услуги: ",
            justify="left",
            anchor="w",
            font=FONT_BOLD
        )
        service_type_label_text = ctk.CTkLabel(
            row_header,
            text=self.type,
            justify="left",
            anchor="w",
            font=FONT_BOLD
        )
        service_type_label.grid(row=0, column=0, sticky="w", padx=8, pady=8)
        service_type_label_text.grid(row=0, column=1, sticky="w", padx=8, pady=8)

        service_line_label = ctk.CTkLabel(
            row_header,
            text="Линия услуг: ",
            justify="left",
            anchor="w",
            font=FONT_BOLD
        )
        service_line_box = ctk.CTkComboBox(
            row_header,
            values=[serv["name"] for serv in service_lines["data"]],
            justify="left",
            font=FONT,
            variable=self.service_line,
            width=300

        )
        service_line_label.grid(row=1, column=0, sticky="w", padx=8, pady=8)
        service_line_box.grid(row=1, column=1, sticky="w", padx=8, pady=8)

        service_name_label = ctk.CTkLabel(
            row_header,
            text="Название услуги: ",
            justify="left",
            anchor="w",
            font=FONT_BOLD
        )
        service_name_label_text = ctk.CTkEntry(
            row_header,
            font=FONT,
            width=200,
            textvariable=self.service_name
        )
        service_name_label.grid(row=2, column=0, sticky="w", padx=8, pady=8)
        service_name_label_text.grid(row=2, column=1, sticky="w", padx=8, pady=8)

        service_desc_label = ctk.CTkLabel(
            row_header,
            text="Описание услуги: ",
            justify="left",
            anchor="w",
            font=FONT_BOLD
        )
        service_desc_label_text = ctk.CTkEntry(
            row_header,
            font=FONT,
            width=400,
            textvariable=self.service_description
        )
        service_desc_label.grid(row=3, column=0, sticky="w", padx=8, pady=8)
        service_desc_label_text.grid(row=3, column=1, sticky="w", padx=8, pady=8)

        # Footer
        footer_frame = ctk.CTkFrame(main_frame)
        footer_frame.pack(fill="both")

        create_btn = ctk.CTkButton(
            footer_frame,
            text="Создать",
            command=self.create_service
        )
        create_btn.grid(row=0, column=3, padx=8, pady=5)

    def create_service(self):
        token = self.token
        service_type = self.type
        service_line = self.service_line.get()
        service_name = self.service_name.get()
        service_description = self.service_description.get()

        response = post_create_service(
            token=token,
            type_name=service_type,
            line_name=service_line,
            name=service_name,
            description=service_description
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


