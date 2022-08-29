from tkinter import Canvas

def MyCanvas():
    return Canvas(
        bg = "#00EFFF",
        height = 768,
        width = 1024,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )