import re
import json
import re
import numpy as np
import cv2
import os
import datetime
import time
from PIL import Image, ImageDraw
from pathlib import Path

class Time():
    def __init__(self) -> None:
        pass

    def datetime(self):
        now = datetime.datetime.now()
        dt = self.format_datetime(now)
        return dt

    def time(self, dt):
        dt = self.format_datetime(dt)
        dt = str(dt).split('_')[1]
        dt = dt.split('-')
        return '{}:{}'.format(dt[0], dt[1])

    def now(self):
        return time.time()

    def format_datetime(self, dt):
        dt = str(dt).split('.')[0]
        dt = re.sub(' ', '_', dt)
        dt = re.sub(':', '-', dt)
        return dt

class ProcessImage():
    def __init__(self) -> None:
        pass

    def jpg_to_png(self, img, size=(459, 461)):
        OUTPUT_PATH = Path(__file__).parent.parent
        img = cv2.resize(img, size)
        img = Image.fromarray(img).convert('RGB')
        h, w = img.size
        np_img = np.asarray(img)

        alpha = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(alpha)
        draw.pieslice([0, 0, h, w], 0, 360, fill=255)

        np_alpha = np.asarray(alpha)
        np_img = np.dstack((np_img, np_alpha))
        parent_path = os.path.join(os.getcwd(), "clipboard")
        Path(parent_path).mkdir(parents=True, exist_ok=True)

        Image.fromarray(np_img).save(os.path.join(parent_path, "result.png"))

def get_model_info():
    file_name = os.path.join(os.getcwd(), 'database/model.json')
    jfile = open(file_name)
    model_infos = json.load(jfile)
    return  model_infos['model_name'], \
            os.path.join(os.getcwd(), model_infos['representation_path'])