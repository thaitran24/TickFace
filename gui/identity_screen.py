from pathlib import Path
from tkinter import DISABLED, Button, PhotoImage
from tkinter.font import NORMAL

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class IdentityScreenWidget():
    def __init__(self, canvas):
        self.canvas = canvas

        self.img = PhotoImage(
            file=relative_to_assets("image.png"))

        self.yesImg = PhotoImage(
            file=relative_to_assets("yes.png"))
        self.yesButton = Button(
            image=self.yesImg,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.noImg = PhotoImage(
            file=relative_to_assets("no.png"))
        self.noButton = Button(
            image=self.noImg,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        
    def setWindow(self, window):
        self.canvas.master = window
    
    def enable(self):
        self.canvas.create_image(
            512.0,
            264.0,
            image=self.img
        )

        self.yesButton.place(
            x=265.0,
            y=649.0,
            width=100.0,
            height=100.0
        )

        self.noButton.place(
            x=659.0,
            y=649.0,
            width=100.0,
            height=100.0
        )

        self.canvas.create_rectangle(
            138.0,
            522.0,
            888.0,
            622.0,
            fill="#FFFFFF",
            outline=""
        )
        self.enableButton()
    
    def disable(self):
        self.disableButton()
        self.noButton.place_forget()
        self.yesButton.place_forget()
        self.canvas.delete('all')

    def setYesTransfer(self, func):
        self.yesButton.configure(command=func)
    
    def setNoTransfer(self, func):
        self.noButton.configure(command=func)
    
    def setText(self, text):
        textPixelLength = 16 * len(text)
        x = 512 - textPixelLength / 2
        self.canvas.create_text(
            x,
            548.0,
            anchor="nw",
            text=text,
            fill="#242424",
            font=("MS Sans Serif", 32 * -1),
            justify='center'
        )
    
    def setImage(self, imgPath):
        self.img = PhotoImage(file=imgPath)
        self.canvas.create_image(
            512.0,
            264.0,
            image=self.img
        )
    
    def enableButton(self):
        self.yesButton.configure(state=NORMAL)
        self.noButton.configure(state=NORMAL)
    
    def disableButton(self):
        self.yesButton.configure(state=DISABLED)
        self.noButton.configure(state=DISABLED)
