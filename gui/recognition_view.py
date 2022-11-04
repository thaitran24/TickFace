from PIL import Image, ImageTk
from tkinter import CENTER, Label
from facereglib import Recognizer
from utils import Time, ProcessImage, get_model_info
import cv2

class RecognitionScreenWid():
    def __init__(self, window):
        # self.window = window
        self.label = Label(window)
        self.label.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    def set_frame(self, frame):
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        self.label.update()

    def disable(self):
        self.label.destroy()


class RecognitionScreen():
    def __init__(self, window):
        self.recog_screen = RecognitionScreenWid(window)
        model_name, representation_path = get_model_info()
        self.model = Recognizer(model_name=model_name, representation_path=representation_path)
        self.exit_flag = False
        window.protocol("WM_DELETE_WINDOW", self.handle_exit)

    def start_recognition(self):
        self.update()
    
    def update(self, *args):
        self.capture = cv2.VideoCapture(0)
        cap_w = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        cap_h = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        w = int(cap_w * 0.6)
        h = int(cap_h * 0.8)
        x = int((cap_w - w) / 2)
        y = int((cap_h - h) / 2)
        in_area = 0.4 * w * h

        in_frame_time = 3
        frame_include_face = False
        in_frame_tic = Time().now()
        curr_time = Time().datetime()

        while True:
            success, frame = self.capture.read()
            if not success:
                break

            # frame = cv2.rotate(frame, cv2.ROTATE_180)   # rotate 180 because of pi camera
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if self.exit_flag:
                return False

            self.recog_screen.set_frame(frame)
            img_frame = frame[y : y + h, x : x + w]

            detected_faces, regions = self.model.detector.detect(img_frame)
            detected_faces_len = len(detected_faces)
            
            if detected_faces_len == 0:
                in_frame_tic = Time().now()
            
            if detected_faces_len > 0:
                face = detected_faces[0]
                if (face.shape[0] * face.shape[1] > in_area):
                    in_frame_toc = Time().now()
                    if (in_frame_toc - in_frame_tic > in_frame_time):
                        frame_include_face = True
                else:
                    in_frame_tic = Time().now()

            if frame_include_face:
                curr_time = Time().datetime()
                face = detected_faces[0]
                self.recog_info = self.model.recognize(face)
                self.recog_info['time'] = curr_time
                self.img_frame = img_frame
                ProcessImage().jpg_to_png(img_frame)
                self.release()
        
        return True
    
    def handle_exit(self):
        self.exit_flag = True
        self.recog_screen.label.master.destroy()

    def release(self):
        self.capture.release()
        cv2.destroyAllWindows()
        self.recog_screen.disable()
    
    def on_release(self, func):
        self.func = func
        
    def get_recog_info(self):
        return self.recog_info, self.img_frame
