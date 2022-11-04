from tkinter import DISABLED, Button, PhotoImage
from tkinter.font import NORMAL
from gui.access_path import relative_to_assets

class IdentityScreen():
    def __init__(self, canvas, window):
        self.canvas = canvas
        self.canvas.master = window

        self.img = PhotoImage(
            file=relative_to_assets("image.png"))

        self.yes_img = PhotoImage(
            file=relative_to_assets("yes.png"))
        self.yes_button = Button(
            image=self.yes_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.no_img = PhotoImage(
            file=relative_to_assets("no.png"))
        self.no_button = Button(
            image=self.no_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
    
    def enable(self):
        self.canvas.create_image(
            512.0,
            248.0,
            image=self.img
        )

        self.yes_button.place(
            x=266.0,
            y=613.0,
            width=100.0,
            height=100.0
        )

        self.no_button.place(
            x=660.0,
            y=613.0,
            width=100.0,
            height=100.0
        )

        self.canvas.create_rectangle(
            137.0,
            498.0,
            887.0,
            598.0,
            fill="#FFFFFF",
            outline=""
        )
        self.enableButton()
    
    def disable(self):
        self.disableButton()
        self.no_button.place_forget()
        self.yes_button.place_forget()
        self.canvas.delete('all')

    def set_yes_btn_trans(self, func):
        self.yes_button.configure(command=func)
    
    def set_no_btn_trans(self, func):
        self.no_button.configure(command=func)
    
    def set_text(self, text):
        text_px_len = 16 * len(text)
        x = 512 - text_px_len / 2
        self.canvas.create_text(
            x,
            524.0,
            anchor="nw",
            text=text,
            fill="#242424",
            font=("MS Sans Serif", 32 * -1),
            justify='center'
        )
    
    def set_image(self, img_path):
        self.img = PhotoImage(file=img_path)
        self.canvas.create_image(
            512.0,
            248.0,
            image=self.img
        )
    
    def enableButton(self):
        self.yes_button.configure(state=NORMAL)
        self.no_button.configure(state=NORMAL)
    
    def disableButton(self):
        self.yes_button.configure(state=DISABLED)
        self.no_button.configure(state=DISABLED)
