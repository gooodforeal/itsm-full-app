import customtkinter
import customtkinter as ctk


FONT_BOLD = ("Segoe UI", 14, "bold")
FONT = ("Segoe UI", 14)


class ServiceForm(ctk.CTkToplevel):
    def __init__(self, parent, service) -> None:
        super().__init__()
        WIDTH = self.winfo_screenwidth()
        HEIGHT = self.winfo_screenheight()
        WIDTH = WIDTH // 2
        HEIGHT = HEIGHT // 2
        WIDTH = WIDTH - 200
        HEIGHT = HEIGHT - 200
        self.geometry(f'1200x700+{WIDTH}+{HEIGHT}')

        self.parent = parent
        self.service = service

        self.resizable(False, False)

        self.title("PCBoost")

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.draw_widgets()
        self.grab_focus()

    def draw_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=1, fill="both")

        if self.service["status"] == "ok":
            # Row service id
            row_header = ctk.CTkFrame(main_frame)
            row_header.pack(expand=1, fill="both", anchor="n")

            service_id_label = ctk.CTkLabel(
                row_header,
                text="ID: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            service_id_label_text = ctk.CTkLabel(
                row_header,
                text=self.service["data"]["id"],
                justify="left",
                anchor="w",
                font=FONT

            )
            service_id_label.grid(row=0, column=0, sticky="w", padx=8, pady=8)
            service_id_label_text.grid(row=0, column=1, sticky="w", padx=8, pady=8)

            # Row service
            service_type_label = ctk.CTkLabel(
                row_header,
                text="Тип услуги: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            service_type_text = ctk.CTkLabel(
                row_header,
                text=self.service["data"]["service_type"]["name"],
                justify="left",
                anchor="w",
                font=FONT
            )
            service_type_label.grid(row=1, column=0, sticky="w", padx=8, pady=8)
            service_type_text.grid(row=1, column=1, sticky="w", padx=8, pady=8)

            # Row service line
            service_line_label = ctk.CTkLabel(
                row_header,
                text="Линия услуг: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            service_line_label_text = ctk.CTkLabel(
                row_header,
                text=self.service["data"]["service_line"]["name"],
                justify="left",
                anchor="w",
                font=FONT
            )
            service_line_label.grid(row=2, column=0, sticky="w", padx=8, pady=8)
            service_line_label_text.grid(row=2, column=1, sticky="w", padx=8, pady=8)

            # Row service name
            service_name_label = ctk.CTkLabel(
                row_header,
                text="Название услуги: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            service_name_label_text = ctk.CTkLabel(
                row_header,
                text=self.service["data"]["name"],
                justify="left",
                anchor="w",
                font=FONT
            )
            service_name_label.grid(row=3, column=0, sticky="w", padx=8, pady=8)
            service_name_label_text.grid(row=3, column=1, sticky="w", padx=8, pady=8)

            # Row service desc
            service_desc_label = ctk.CTkLabel(
                row_header,
                text="Описание услуги: ",
                justify="left",
                anchor="w",
                font=FONT_BOLD
            )
            service_desc_label_text = ctk.CTkLabel(
                row_header,
                text=self.service["data"]["description"].replace("; ", "\n"),
                justify="left",
                anchor="w",
                font=FONT
            )
            service_desc_label.grid(row=4, column=0, sticky="w", padx=8, pady=8)
            service_desc_label_text.grid(row=4, column=1, sticky="w", padx=8, pady=8)

        else:
            error_label = ctk.CTkLabel(
                main_frame,
                text=self.service["message"]
            )
            error_label.pack()

    def grab_focus(self) -> None:
        self.grab_set()
        self.parent.wait_window(self)

    def run_app(self) -> None:
        self.mainloop()


