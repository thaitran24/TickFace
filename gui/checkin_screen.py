from pathlib import Path
from tkinter import Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class CheckinScreenWidget():
    def __init__(self, canvas):
        self.canvas = canvas

        self.img = PhotoImage(
            file=relative_to_assets("image.png"))

        self.checkinImg = PhotoImage(
            file=relative_to_assets("checkin.png"))
        self.checkinButton = Button(
            image=self.checkinImg,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.checkoutImg = PhotoImage(
            file=relative_to_assets("checkout.png"))
        self.checkoutButton = Button(
            image=self.checkoutImg,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
    
    def enable(self):
        self.canvas.create_image(
            512.0,
            264.0,
            image=self.img
        )
        self.canvas.create_rectangle(
            138.0,
            522.0,
            888.0,
            622.0,
            fill="#FFFFFF",
            outline=""
        )
        self.canvas.create_text(
            247.0,
            548.0,
            anchor="nw",
            text="You wanna check-in or check-out?",
            fill="#242424",
            font=("Mplus1p Medium", 32 * -1)
        )
        self.checkinButton.place(
            x=158.0,
            y=649.0,
            width=250.0,
            height=80.0
        )
        self.checkoutButton.place(
            x=617.0,
            y=649.0,
            width=250.0,
            height=80.0
        )
    
    def disable(self):
        self.canvas.delete('all')
        self.checkinButton.place_forget()
        self.checkoutButton.place_forget()
    
    def setCheckinTransfer(self, func):
        self.checkinButton.configure(command=func)
    
    def setCheckoutTransfer(self, func):
        self.checkoutButton.configure(command=func)
    
    def setWindow(self, window):
        self.canvas.master = window
    
    def setImage(self, imgPath):
        self.img = PhotoImage(file=imgPath)
        self.canvas.create_image(
            512.0,
            264.0,
            image=self.img
        )