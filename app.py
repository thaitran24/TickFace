from gui.main_screen import MainScreenWidget
from gui.recognition_screen import RecognitionScreenWidget
from gui.identity_screen import IdentityScreenWidget
from gui.checkin_screen import CheckinScreenWidget
from gui.realname_screen import RealnameScreenWidget
from gui.thanks_screen import ThanksScreenWidget
from gui.canvas import MyCanvas
from tkinter import Tk
from facereglib.facereg.recognizer import Recognizer
from database.database import Database
from api import slack_post
import time
import cv2
import datetime
import utils

class RecognitionScreen():
    def __init__(self, window):
        self.recogScreenWids = RecognitionScreenWidget(window)
        model_name, database_folder, representation_folder = utils.getModelInfo()
        self.model = Recognizer(model_name=model_name, db_represent_path=representation_folder)
        
    def startRecognition(self):
        self.update()
    
    def update(self, *args):
        self.capture = cv2.VideoCapture(0)
        capW = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        capH = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        w = int(capW * 0.6)
        h = int(capH * 0.8)
        x = int((capW - w) / 2)
        y = int((capH - h) / 2)
        inArea = 0.4 * w * h

        inFrameTime = 3
        frameIncludeFace = False
        inFrameTic = time.time()
        currTime = datetime.datetime.now()

        while True:
            success, frame = self.capture.read()
            if not success:
                break
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.recogScreenWids.setFrame(frame)
            imgFrame = frame[y : y + h, x : x + w]

            detectedFaces, regions = self.model.detector.detect(imgFrame)
            detectedFacesLen = len(detectedFaces)
            
            if detectedFacesLen == 0:
                inFrameTic = time.time()
            
            if detectedFacesLen > 0:
                face = detectedFaces[0]
                if (face.shape[0] * face.shape[1] > inArea):
                    inFrameToc = time.time()
                    if (inFrameToc - inFrameTic > inFrameTime):
                        frameIncludeFace = True
                else:
                    inFrameTic = time.time()

            if frameIncludeFace:
                currTime = datetime.datetime.now()
                face = detectedFaces[0]
                self.recogInfo = Database().getRecogInfo(self.model.recognize(face))
                self.recogInfo['time'] = currTime
                self.imgFrame = imgFrame
                utils.JPGtoPNG(imgFrame)
                self.release()
    
    def release(self):
        self.capture.release()
        cv2.destroyAllWindows()
        self.recogScreenWids.disable()
        
    def getRecogInfo(self):
        return self.recogInfo, self.imgFrame


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
        self.mainScreenWids.setTransfer(self.MainScreenToRecogScreen)
        
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
        self.recogScreen.startRecognition()
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
   