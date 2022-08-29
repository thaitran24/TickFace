from pathlib import Path
from tkinter import Button, PhotoImage

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

        self.logoImg = PhotoImage(
            file=relative_to_assets("logo.png"))
        
    def run(self):
        return self.status

    def setTransfer(self, func):
        self.startButton.configure(command=func)

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
            font=("Ubuntu", 72 * -1)
        )

        self.startButton.place(
            x=288.0,
            y=571.0,
            width=449.0,
            height=103.0
        )

    def disable(self):
        self.startButton.place_forget()
        self.canvas.delete('all')
        
    def setWindow(self, window):
        self.canvas.master = window