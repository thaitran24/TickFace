from gui.main_screen import MainScreenWidget
from gui.recognition_screen import RecognitionScreenWidget
from gui.identity_screen import IdentityScreenWidget
from gui.checkin_screen import CheckinScreenWidget
from gui.realname_screen import RealnameScreenWidget
from gui.thanks_screen import ThanksScreenWidget
from gui.canvas import MyCanvas
from tkinter import Image, Tk
from facereglib.facereg.recognizer import Recognizer
from database.database import Database
from api import slack_post
from PIL import Image
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
        self.capture = cv2.VideoCapture(0)
        self.initFrameSettings()
        self.initFaceInFrameSettings()
        self.update()

    def initFrameSettings(self):
        self.inFrameTime = 3

        capW = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        capH = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.w = int(capW * 0.6)
        self.h = int(capH * 0.8)
        self.x = int((capW - self.w) / 2)
        self.y = int((capH - self.h) / 2)

        self.in_area = 0.4 * self.w * self.h

    def initFaceInFrameSettings(self):
        self.inRecogPhase = False
        self.frameIncludeFace = False
        self.inFrameTic = time.time()
        self.tic = time.time()
        self.toc = time.time()
        self.now = datetime.datetime.now()
    
    def update(self, *args):
        while True:
            success, frame = self.capture.read()
            if not success:
                break
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.recogScreenWids.setFrame(frame)
            imgFrame = frame[self.y : self.y + self.h, self.x : self.x + self.w]

            if not self.inRecogPhase:
                detected_faces, regions = self.model.detector.detect(imgFrame)
            else:
                detected_faces = []
            
            detected_face_len = len(detected_faces)
            
            if detected_face_len == 0:
                self.inFrameTic = time.time()
            
            if detected_face_len > 0:
                face = detected_faces[0]
                if (face.shape[0] * face.shape[1] > self.in_area):
                    in_frame_toc = time.time()
                    if (in_frame_toc - self.inFrameTic > self.inFrameTime):
                        self.frameIncludeFace = True
                else:
                    self.inFrameTic = time.time()

            if detected_face_len > 0 and self.frameIncludeFace and not self.inRecogPhase:
                self.inRecogPhase = True
                self.tic = time.time()
                self.now = datetime.datetime.now()
            
            if self.inRecogPhase:
                face = detected_faces[0]
                self.toc = time.time()
                self.recogInfo = Database().getRecogInfo(self.model.recognize(face))
                self.recogInfo['time'] = self.now
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
        self.window.geometry("1024x768")
        self.window.configure(bg = "#00EFFF")
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
   