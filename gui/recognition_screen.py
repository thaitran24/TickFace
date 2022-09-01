from pathlib import Path
from PIL import ImageTk, Image
from tkinter import CENTER, Label
from facereglib.facereg.recognizer import Recognizer
from database.database import Database
import time
import cv2
import datetime
import utils

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class RecognitionScreenWidget():
    def __init__(self, window):
        # self.window = window
        self.label = Label(window)
        self.label.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    def setFrame(self, frame):
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        self.label.update()

    def disable(self):
        self.label.destroy()


class RecognitionScreen():
    def __init__(self, window):
        self.recogScreenWids = RecognitionScreenWidget(window)
        model_name, database_folder, representation_folder = utils.getModelInfo()
        self.model = Recognizer(model_name=model_name, db_represent_path=representation_folder)
        self.exitFlag = False
        window.protocol("WM_DELETE_WINDOW", self.handleExit)

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
            if self.exitFlag:
                return False

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
        
        return True
    
    def handleExit(self):
        self.exitFlag = True
        self.recogScreenWids.label.master.destroy()

    def release(self):
        self.capture.release()
        cv2.destroyAllWindows()
        self.recogScreenWids.disable()
        
    def getRecogInfo(self):
        return self.recogInfo, self.imgFrame
