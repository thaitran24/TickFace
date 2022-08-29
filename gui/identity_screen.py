from pathlib import Path
from tkinter import Button, PhotoImage

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
    
    def disable(self):
        self.canvas.delete('all')
        self.noButton.place_forget()
        self.yesButton.place_forget()

    def setYesTransfer(self, func):
        self.yesButton.configure(command=func)
    
    def setNoTransfer(self, func):
        self.noButton.configure(command=func)
    
    def setText(self, text):
        self.canvas.create_text(
            316.0,
            548.0,
            anchor="nw",
            text=text,
            fill="#242424",
            font=("Mplus1p Medium", 32 * -1),
            justify='center'
        )
    
    def setImage(self, imgPath):
        self.img = PhotoImage(file=imgPath)
        self.canvas.create_image(
            512.0,
            264.0,
            image=self.img
        )