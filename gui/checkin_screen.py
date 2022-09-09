from pathlib import Path
from tkinter import DISABLED, Button, PhotoImage
from tkinter.font import NORMAL

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
        self.checkinButton.place(
            x=158.0,
            y=617.0,
            width=250.0,
            height=80.0
        )
        self.checkoutButton.place(
            x=617.0,
            y=617.0,
            width=250.0,
            height=80.0
        )
        self.enableButton()
    
    def disable(self):
        self.disableButton()
        self.checkinButton.place_forget()
        self.checkoutButton.place_forget()
        self.canvas.delete('all')
    
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
            248.0,
            image=self.img
        )
    
    def enableButton(self):
        self.checkinButton.configure(state=NORMAL)
        self.checkoutButton.configure(state=NORMAL)
    
    def disableButton(self):
        self.checkinButton.configure(state=DISABLED)
        self.checkoutButton.configure(state=DISABLED)