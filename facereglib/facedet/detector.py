from facereglib.facedet.models import BlazeFace, Mediapipe
import cv2
import numpy as np
import math
from PIL import Image

class Detector():
    def __init__(self, model_name='BlazeFace') -> None:
        det_models = {
            'BlazeFace': BlazeFace,
            'DeepFace': Mediapipe
        }
        base_model = det_models.get(model_name)
        if not base_model:
            raise ValueError("Invalid model_name passed - {}".format(model_name))
        
        self.model_name = model_name
        self.model = base_model()
    
    def detect(self, img):
        return self.model.detect(img)
    
    