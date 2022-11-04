from tkinter import DISABLED, Button, PhotoImage
from tkinter.font import NORMAL
from gui.access_path import relative_to_assets

class CheckinScreen():
    def __init__(self, canvas, window):
        self.canvas = canvas
        self.canvas.master = window

        self.img = PhotoImage(
            file=relative_to_assets("image.png"))

        self.checkin_img = PhotoImage(
            file=relative_to_assets("checkin.png"))
        self.checkin_button = Button(
            image=self.checkin_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.checkout_img = PhotoImage(
            file=relative_to_assets("checkout.png"))
        self.checkout_button = Button(
            image=self.checkout_img,
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
        self.canvas.create_rectangle(
            137.0,
            498.0,
            887.0,
            598.0,
            fill="#FFFFFF",
            outline=""
        )
        self.canvas.create_text(
            246.0,
            524.0,
            anchor="nw",
            text="You wanna check-in or check-out?",
            fill="#242424",
            font=("MS Sans Serif", 32 * -1)
        )
        self.checkin_button.place(
            x=158.0,
            y=617.0,
            width=250.0,
            height=80.0
        )
        self.checkout_button.place(
            x=617.0,
            y=617.0,
            width=250.0,
            height=80.0
        )
        self.enable_button()
    
    def disable(self):
        self.disable_button()
        self.checkin_button.place_forget()
        self.checkout_button.place_forget()
        self.canvas.delete('all')
    
    def set_checkin_btn_trans(self, func):
        self.checkin_button.configure(command=func)
    
    def set_checkout_btn_trans(self, func):
        self.checkout_button.configure(command=func)
    
    def set_image(self, img_path):
        self.img = PhotoImage(file=img_path)
        self.canvas.create_image(
            512.0,
            248.0,
            image=self.img
        )
    
    def enable_button(self):
        self.checkin_button.configure(state=NORMAL)
        self.checkout_button.configure(state=NORMAL)
    
    def disable_button(self):
        self.checkin_button.configure(state=DISABLED)
        self.checkout_button.configure(state=DISABLED)