import re
import json
import re
import numpy as np
import cv2
from PIL import Image, ImageDraw
from pathlib import Path

def dateTimeStr(dt):
    dt = str(dt).split('.')[0]
    dt = re.sub(' ', '_', dt)
    dt = re.sub(':', '-', dt)
    return dt


def getTime(dt):
    dt = str(dt).split(' ')[1]
    dt = dt.split(':')
    return dt[0] + ':' + dt[1]


def getModelInfo():
    file_name = 'database/model_info.json'
    jfile = open(file_name)
    model_infos = json.load(jfile)
    return model_infos['model_name'], model_infos['database_folder'], model_infos['representation_folder']


def JPGtoPNG(npImg, size=(459, 461)):
    img = cv2.resize(npImg, size)
    img = Image.fromarray(img).convert('RGB')
    h, w = img.size
    npImg = np.asarray(img)

    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)

    npAlpha = np.asarray(alpha)
    npImg = np.dstack((npImg,npAlpha))
    Path('clipboard').mkdir(parents=True, exist_ok=True)

    Image.fromarray(npImg).save('clipboard/result.png')