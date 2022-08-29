from pathlib import Path
from PIL import ImageTk, Image
from tkinter import CENTER, Label, Frame

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class RecognitionScreenWidget():
    def __init__(self, window):
        self.window = window
        self.label = Label(self.window)
        self.label.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    def setFrame(self, frame):
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        self.label.update()

    def disable(self):
        self.label.destroy()

