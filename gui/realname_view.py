from tkinter import END, Entry, PhotoImage
from gui.access_path import relative_to_assets

class RealnameScreen():
    def __init__(self, canvas, window):
        self.canvas = canvas
        self.canvas.master = window

        self.img = PhotoImage(
            file=relative_to_assets("image.png"))

        self.entry_img = PhotoImage(
            file=relative_to_assets("entry.png"))
        self.entry_button = Entry(
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

        self.entry_bg = self.canvas.create_image(
            512.0,
            660.0,
            image=self.entry_img
        )

        self.entry_button.place(
            x=292.0,
            y=630.0,
            width=440.0,
            height=58.0
        )

        self.entry_button.delete(0, END)
    
    def disable(self):
        self.canvas.delete('all')
        self.entry_button.place_forget()
    
    def set_entry_btn_trans(self, func):
        self.entry_button.bind('<Return>', func=func)
    
    def get_entry(self):
        return self.entry_button.get()
    
    def set_image(self, img_path):
        self.img = PhotoImage(file=img_path)
        self.canvas.create_image(
            512.0,
            264.0,
            image=self.img
        )

    
        
