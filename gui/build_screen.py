from tkinter import CENTER, DISABLED, END, filedialog, Listbox, Toplevel, PhotoImage, Button
from tkinter.font import NORMAL
from tkinter.messagebox import YES
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class DirectoryDialog():
    def __init__(self):
        self.enable()

    def enable(self):
        self.directory = filedialog.askdirectory(title="Choose Database Image Directory")

    def getDirectory(self):
        return self.directory

class ModelDialog():
    def __init__(self, window, choices):
        self.top = Toplevel(window)
        self.top.title("Select Model")
        self.top.resizable(False, False)
        self.top.protocol("WM_DELETE_WINDOW", func=self.ignore)
        self.choices = choices
        self.list = Listbox(self.top, font=("MS Sans Serif", 28 * -1), fg="#242424", justify=CENTER)
        self.list.pack(expand=YES, fill="both")
        for item in range(len(self.choices)):
            self.list.insert(END, self.choices[item])
        
    def setTransfer(self, func):
        self.list.bind('<Double-Button-1>', func=func)

    def getChoice(self):
        index = self.list.curselection()
        self.selectedChoice = self.choices[index[0]]
        return self.selectedChoice
    
    def disable(self):
        self.top.destroy()
    
    def ignore(self):
        pass

class BuildScreenWidget():
    def __init__(self, canvas):
        self.canvas = canvas

        self.buildImg = PhotoImage(
            file=relative_to_assets("buildButton.png"))
        self.buildButton = Button(
            image=self.buildImg,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )

        self.chooseDirImg = PhotoImage(
            file=relative_to_assets("chooseDirButton.png"))
        self.chooseDirButton = Button(
            image=self.chooseDirImg,
            borderwidth=0,
            highlightthickness=0,
            command=self.directoryDialog,
            relief="flat"
        )

        self.chooseModelImg = PhotoImage(
            file=relative_to_assets("chooseModelButton.png"))
        self.chooseModelButton = Button(
            image=self.chooseModelImg,
            borderwidth=0,
            highlightthickness=0,
            command=self.modelDialog,
            relief="flat"
        )

        self.logoImg = PhotoImage(
            file=relative_to_assets("logo.png"))
        
        self.checkImg = PhotoImage(
            file=relative_to_assets("check.png"))

        self.text = ''

    def setWindow(self, window):
        self.canvas.master = window
    
    def enable(self):
        self.buildButton.place(
            x=335.0,
            y=581.0,
            width=354.0,
            height=72.0
        )
        self.chooseDirButton.place(
            x=93.0,
            y=384.0,
            width=354.0,
            height=103.0
        )
        self.chooseModelButton.place(
            x=575.0,
            y=384.0,
            width=354.0,
            height=103.0
        )
        self.canvas.create_image(
            512.0,
            187.0,
            image=self.logoImg
        )
        self.enableButton()

    def checkDir(self):
        self.canvas.create_image(
            270.0,
            529.0,
            image=self.checkImg
        )
    
    def checkModel(self):
        self.canvas.create_image(
            752.0,
            529.0,
            image=self.checkImg
        )

    def disable(self):
        self.disableButton()
        self.buildButton.place_forget()
        self.chooseDirButton.place_forget()
        self.chooseModelButton.place_forget()
        self.canvas.delete('all')

    def setBuildTransfer(self, func):
        self.buildButton.configure(command=func)
    
    def directoryDialog(self):
        self.disableButton()
        self.directory = DirectoryDialog().getDirectory()
        self.enableButton()
        if self.directory:
            print(self.directory)
            self.checkDir()

    def modelDialog(self):
        self.disableButton()
        models = ['VGG-Face', 'Facenet', 'DeepFace', 'DeepID', 'ArcFace']
        self.modelDialog = ModelDialog(self.canvas.master, models)
        self.modelDialog.setTransfer(self.handleModelInput)

    def handleModelInput(self, *args):
        self.modelName = self.modelDialog.getChoice()
        if self.modelName:
            print(self.modelName)
            self.checkModel()
        self.enableButton()
        self.modelDialog.disable()

    def setText(self, text):
        self.canvas.delete(self.text)
        self.text = self.canvas.create_text(
            418.0,
            681.0,
            anchor="nw",
            text=text,
            fill="#242424",
            font=("MS Sans Serif", 22 * -1)
        )
        
    def getDirectory(self):
        return self.directory

    def getModel(self):
        return self.modelName
    
    def enableButton(self):
        self.buildButton.configure(state=NORMAL)
        self.chooseDirButton.configure(state=NORMAL)
        self.chooseModelButton.configure(state=NORMAL)

    def disableButton(self):
        self.buildButton.configure(state=DISABLED)
        self.chooseDirButton.configure(state=DISABLED)
        self.chooseModelButton.configure(state=DISABLED)
