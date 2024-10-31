import customtkinter
import customtkinter as ctk

from tkinter import ttk
from tkinter.messagebox import showerror

from tkinter import StringVar

from client.api_requests.dialogs.dialogs import get_messages, post_send_message

FONT_BOLD = ("Segoe UI", 14, "bold")
FONT = ("Segoe UI", 14)
FONT_DATE = ("Segoe UI", 9)


class DialogForm(ctk.CTkToplevel):
    def __init__(self, parent, token, recipient_username) -> None:
        super().__init__()

        self.geometry('1000x800')

        self.parent = parent
        self.token = token
        self.recipient_username = recipient_username

        self.frame = None
        self.messages = None
        self.canvas = None
        self.vsb = None

        self.enter = StringVar()

        self.resizable(False, False)

        self.title("Чат")

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.draw_widgets()
        self.grab_focus()

    def draw_messages(self):
        messages = get_messages(token=self.token, recipient_username=self.recipient_username)

        if messages != self.messages:
            self.messages = messages

            for child in self.frame.winfo_children():
                child.destroy()

            i = 0
            if len(self.messages):
                for msg in self.messages["data"]:
                    if msg["sender"]["username"] == self.recipient_username:
                        msgrow = ctk.CTkFrame(self.frame)

                        msg_label = ctk.CTkLabel(
                            msgrow,
                            text=f'{self.recipient_username}: ',
                            justify="left",
                            anchor="w",
                            font=FONT_BOLD
                        )
                        msg_label_text = ctk.CTkLabel(
                            msgrow,
                            text=msg["message"],
                            justify="left",
                            anchor="w",
                            font=FONT
                        )
                        time_label_text = ctk.CTkLabel(
                            msgrow,
                            text=msg["created_at"].split(".")[0].replace("T", " ")[:-3],
                            justify="left",
                            anchor="w",
                            font=FONT_DATE
                        )
                        msg_label.grid(row=i, column=0, sticky="w", padx=8, pady=8)
                        msg_label_text.grid(row=i, column=1, sticky="w", padx=8, pady=8)

                        time_label_text.grid(row=i, column=2, sticky="w", padx=8, pady=8)

                        msgrow.pack(anchor="nw", pady=10, padx=10)
                    else:
                        msgrow = ctk.CTkFrame(self.frame)

                        msg_label = ctk.CTkLabel(
                            msgrow,
                            text=f'{msg["sender"]["username"]}: ',
                            justify="right",
                            anchor="e",
                            font=FONT_BOLD
                        )

                        msg_label_text = ctk.CTkLabel(
                            msgrow,
                            text=msg["message"],
                            justify="left",
                            anchor="w",
                            font=FONT
                        )

                        time_label_text = ctk.CTkLabel(
                            msgrow,
                            text=msg["created_at"].split(".")[0].replace("T", " ")[:-3],
                            justify="right",
                            anchor="e",
                            font=FONT_DATE
                        )
                        msg_label.grid(row=i, column=0, sticky="w", padx=8, pady=8)
                        msg_label_text.grid(row=i, column=1, sticky="w", padx=8, pady=8)

                        time_label_text.grid(row=i, column=2, sticky="w", padx=8, pady=8)

                        msgrow.pack(anchor="ne", pady=10, padx=10)

        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.after(3000, self.draw_messages)

    def draw_widgets(self):
        self.canvas = ctk.CTkCanvas(self, borderwidth=0)
        self.frame = ctk.CTkFrame(self.canvas, bg_color="#ffffff")
        self.vsb = ttk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.configure(bg='grey20')
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.create_window(0, 0, window=self.frame, anchor="n", width=985)

        self.draw_messages()



        footer_row = ctk.CTkFrame(self)

        create_button = ctk.CTkButton(
            footer_row,
            text="Отправить",
            command=self.send_message
        )
        create_button.grid(row=0, column=1, padx=8, pady=5)

        enter_entry = ctk.CTkEntry(
            footer_row,
            textvariable=self.enter,
            font=FONT,
            height=50,
            width=800
        )
        enter_entry.grid(row=0, column=0, padx=8, pady=5)

        footer_row.pack(fill="both")

    def send_message(self):
        if len(self.enter.get()) < 1:
            showerror(title="Error", message="To short message!")
        else:
            post_send_message(
                token=self.token,
                recipient_username=self.recipient_username,
                message=self.enter.get()
            )

    def grab_focus(self) -> None:
        self.grab_set()
        self.parent.wait_window(self)

    def run_app(self) -> None:
        self.mainloop()


