from gui.main_screen import MainScreenWidget
from gui.recognition_screen import RecognitionScreen
from gui.identity_screen import IdentityScreenWidget
from gui.checkin_screen import CheckinScreenWidget
from gui.realname_screen import RealnameScreenWidget
from gui.thanks_screen import ThanksScreenWidget
from gui.build_screen import BuildScreenWidget
from gui.canvas import MyCanvas
from tkinter import Tk
from database.database import Database, ModelBuilder
from api import slack_post
import utils
class App():
    def __init__(self):
        self.initLayout()
        self.database = Database()

    def initLayout(self):
        self.window = Tk()
        self.window.title('TickFace')
        self.window.geometry('1024x768')
        self.window.configure(bg='#00EFFF')
        self.window.resizable(False, False)

        self.canvas = MyCanvas()
        self.canvas.place(x=0, y=0)

        self.mainScreenWids = MainScreenWidget(self.canvas)
        self.mainScreenWids.setWindow(self.window)
        self.mainScreenWids.setStartTransfer(self.MainScreenToRecogScreen)
        self.mainScreenWids.setBuildTransfer(self.MainSreenToBuildScreen)
        
        self.buildScreenWids = BuildScreenWidget(self.canvas)
        self.buildScreenWids.setWindow(self.window)
        self.buildScreenWids.setBuildTransfer(self.startBuildModel)

        self.idenScreenWids = IdentityScreenWidget(self.canvas)
        self.idenScreenWids.setWindow(self.window)
        self.idenScreenWids.setYesTransfer(self.IdenScreenToCheckinScreen)
        self.idenScreenWids.setNoTransfer(self.IdenScreenToRNScreen)

        self.checkinScreenWids = CheckinScreenWidget(self.canvas)
        self.checkinScreenWids.setWindow(self.window)
        self.checkinScreenWids.setCheckinTransfer(self.confirmCheckin)
        self.checkinScreenWids.setCheckoutTransfer(self.confirmCheckout)
    
        self.realnameScreenWids = RealnameScreenWidget(self.canvas)
        self.realnameScreenWids.setWindow(self.window)
        self.realnameScreenWids.setTransfer(self.RNScreenToCheckinScreen)

        self.thanksScreenWidget = ThanksScreenWidget(self.canvas)

    def run(self):
        self.mainScreen()
        self.window.mainloop()
    
    def mainScreen(self):
        self.mainScreenWids.enable()
    
    def thanksScreen(self):
        self.thanksScreenWidget.enable()
        self.database.writeLog(self.recogInfo, self.imgFrame)
        message = self.recogInfo['realname'] + ' ' + self.recogInfo['check'] + ' at ' + utils.getTime(self.recogInfo['time'])
        slack_post.postMessage(message=message)
        self.window.after(3000, self.ThanksScreenToMainScreen)

    def recognitionScreen(self):
        self.recogScreen = RecognitionScreen(self.window)
        success = self.recogScreen.startRecognition()
        self.recogInfo, self.imgFrame = self.recogScreen.getRecogInfo()
        self.RecogScreenToIdenScreen()
    
    def identityScreen(self):
        self.idenScreenWids.enable()
        text = "Are you " + self.recogInfo['name'] + "?"
        self.idenScreenWids.setText(text=text)
        self.idenScreenWids.setImage('clipboard/result.png')
        self.realnameScreenWids.setImage('clipboard/result.png')
        self.checkinScreenWids.setImage('clipboard/result.png')

    def MainScreenToRecogScreen(self):
        self.mainScreenWids.disable()
        self.window.after(500, self.recognitionScreen)
    
    def MainSreenToBuildScreen(self):
        self.mainScreenWids.disable()
        self.buildScreenWids.enable()

    def startBuildModel(self):
        self.buildScreenWids.setText("Building model...")
        self.buildScreenWids.disableButton()
        self.window.after(500, self.buildModel)
        
    def buildModel(self):
        modelName = self.buildScreenWids.getModel()
        databaseFolder = self.buildScreenWids.getDirectory()
        success = ModelBuilder(modelName, databaseFolder).build()
        if success:
            self.buildScreenWids.setText("Build Successfully!")
        else:
            self.buildScreenWids.setText("Build Failed!")
        self.window.after(2000, self.BuildSreeenToMainScreen)

    def BuildSreeenToMainScreen(self):
        self.buildScreenWids.disable()
        self.mainScreenWids.enable()

    def RecogScreenToIdenScreen(self):
        self.mainScreenWids.disable()
        self.identityScreen()
    
    def IdenScreenToCheckinScreen(self):
        self.idenScreenWids.disable()
        self.recogInfo['realname'] = self.recogInfo['name']
        self.recogInfo['precision'] = True
        self.checkinScreenWids.enable()

    def IdenScreenToRNScreen(self):
        self.idenScreenWids.disable()
        self.recogInfo['precision'] = False
        self.realnameScreenWids.enable()
    
    def RNScreenToCheckinScreen(self, *args):
        realname = self.realnameScreenWids.getEntry()
        self.recogInfo['realname'] = realname
        self.realnameScreenWids.disable()
        self.checkinScreenWids.enable()
    
    def CheckinScreenToThanksScreen(self):
        self.checkinScreenWids.disable()
        self.window.after(500, self.thanksScreen)
    
    def ThanksScreenToMainScreen(self):
        self.thanksScreenWidget.disable()
        self.mainScreen()
    
    def confirmCheckin(self):
        self.recogInfo['check'] = 'check-in'
        self.CheckinScreenToThanksScreen()
    
    def confirmCheckout(self):
        self.recogInfo['check'] = 'check-out'
        self.CheckinScreenToThanksScreen()
    
    def saveLog(self):
        self.database.writeLog(self.recogInfo, self.imgFrame)

if __name__=='__main__':
    app = App()
    app.run()
   