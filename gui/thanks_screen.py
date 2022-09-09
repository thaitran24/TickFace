from pathlib import Path
from tkinter import PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class ThanksScreenWidget():
    def __init__(self, canvas):
        self.canvas = canvas
        self.thanksImg = PhotoImage(
            file=relative_to_assets("thanks.png"))
    
    def enable(self):
        self.canvas.create_image(
            512.0,
            360.0,
            image=self.thanksImg
        )
    
    def disable(self):
        self.canvas.delete('all')
    
