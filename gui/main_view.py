from tkinter import DISABLED, Button, PhotoImage
from tkinter.font import NORMAL
from gui.access_path import relative_to_assets


class MainScreen():
    def __init__(self, canvas, window):
        self.canvas = canvas
        self.canvas.master = window

        self.button_img = PhotoImage(
            file=relative_to_assets("startButton.png"))
        self.start_button = Button(
            image=self.button_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.logo_img = PhotoImage(
            file=relative_to_assets("logo.png"))

    def set_start_btn_trans(self, func):
        self.start_button.configure(command=func)

    def enable(self):
        self.canvas.create_image(
            512.0,
            203.0,
            image=self.logo_img
        )

        self.canvas.create_text(
            335.0,
            368.0,
            anchor="nw",
            text="TICKFACE",
            fill="#242424",
            font=("MS Sans Serif", 72 * -1)
        )

        self.start_button.place(
            x=287.0,
            y=513.0,
            width=449.0,
            height=103.0
        )

        self.enable_button()

    def disable(self):
        self.disable_button()
        self.start_button.place_forget()
        self.canvas.delete('all')

    def enable_button(self):
        self.start_button.configure(state=NORMAL)
    
    def disable_button(self):
        self.start_button.configure(state=DISABLED)