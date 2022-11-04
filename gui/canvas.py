from tkinter import Canvas

def MainCanvas():
    return Canvas(
        bg = "#00EFFF",
        height = 720,
        width = 1024,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )