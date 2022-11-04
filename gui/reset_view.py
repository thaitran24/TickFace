from tkinter import PhotoImage
from gui.access_path import relative_to_assets

class ResetScreen():
    def __init__(self, canvas):
        self.canvas = canvas
        self.reset_img = PhotoImage(
            file=relative_to_assets("thanks.png"))
    
    def enable(self):
        self.canvas.create_image(
            512.0,
            360.0,
            image=self.reset_img
        )
    
    def disable(self):
        self.canvas.delete('all')
    
