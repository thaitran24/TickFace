from pathlib import Path
from tkinter import DISABLED, Button, PhotoImage
from tkinter.font import NORMAL

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class MainScreenWidget():
    def __init__(self, canvas):
        self.canvas = canvas
        
        self.buttonImg = PhotoImage(
            file=relative_to_assets("startButton.png"))
        self.startButton = Button(
            image=self.buttonImg,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.buildButtonImg = PhotoImage(
            file=relative_to_assets("buildButton.png"))
        self.buildButton = Button(
            image=self.buildButtonImg,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.logoImg = PhotoImage(
            file=relative_to_assets("logo.png"))
        
    def run(self):
        return self.status

    def setStartTransfer(self, func):
        self.startButton.configure(command=func)

    def setBuildTransfer(self, func):
        self.buildButton.configure(command=func)

    def enable(self):
        self.canvas.create_image(
            512.0,
            187.0,
            image=self.logoImg
        )

        self.canvas.create_text(
            335.0,
            384.0,
            anchor="nw",
            text="TICKFACE",
            fill="#242424",
            font=("MS Sans Serif", 72 * -1)
        )

        self.startButton.place(
            x=287.0,
            y=511.0,
            width=449.0,
            height=103.0
        )

        self.buildButton.place(
            x=335.0,
            y=639.0,
            width=354.0,
            height=72.0
        )
        self.enableButton()

    def disable(self):
        self.disableButton()
        self.startButton.place_forget()
        self.buildButton.place_forget()
        self.canvas.delete('all')
        
    def setWindow(self, window):
        self.canvas.master = window

    def enableButton(self):
        self.startButton.configure(state=NORMAL)
        self.buildButton.configure(state=NORMAL)
    
    def disableButton(self):
        self.startButton.configure(state=DISABLED)
        self.buildButton.configure(state=DISABLED)