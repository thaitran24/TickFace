from pathlib import Path
from tkinter import END, Entry, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class RealnameScreenWidget():
    def __init__(self, canvas):
        self.canvas = canvas
        self.img = PhotoImage(
            file=relative_to_assets("image.png"))

        self.entryImg = PhotoImage(
            file=relative_to_assets("entry.png"))
        self.entryButton = Entry(
            bd=0,
            bg="#FFFCFC",
            highlightthickness=0,
            justify='center',
            font=("MS Sans Serif", 32 * -1)
        )
    
    def enable(self):
        self.canvas.create_image(
            512.0,
            245.0,
            image=self.img
        )

        self.canvas.create_rectangle(
            137.0,
            497.0,
            887.0,
            597.0,
            fill="#FFFFFF",
            outline=""
        )

        self.canvas.create_text(
            350.0,
            523.0,
            anchor="nw",
            text="Enter your real name",
            fill="#242424",
            font=("MS Sans Serif", 32 * -1)
        )

        self.entryBg = self.canvas.create_image(
            512.0,
            660.0,
            image=self.entryImg
        )

        self.entryButton.place(
            x=292.0,
            y=630.0,
            width=440.0,
            height=58.0
        )

        self.entryButton.delete(0, END)
    
    def disable(self):
        self.canvas.delete('all')
        self.entryButton.place_forget()
    
    def setWindow(self, window):
        self.canvas.master = window
    
    def setTransfer(self, func):
        self.entryButton.bind('<Return>', func=func)
    
    def getEntry(self):
        return self.entryButton.get()
    
    def setImage(self, imgPath):
        self.img = PhotoImage(file=imgPath)
        self.canvas.create_image(
            512.0,
            264.0,
            image=self.img
        )

    
        
