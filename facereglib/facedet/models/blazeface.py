import os
import gdown
import keras.models
import cv2
import numpy as np
import math
from PIL import Image
from facereglib.utils import facedet_utils, distance

def load_model():
    file_path = os.path.join(os.getcwd(), 'facereglib/facedet/weights/')
    file_name = 'blazeface_tf.h5'
    if not os.path.exists(file_path + file_name):
        os.makedirs(file_path, exist_ok=True)
        id = '10REys3sjGpAW8fpLBDc65UxoWeJvE2ye'
        gdown.download(id=id, output=file_path + file_name, quiet=False)
    return keras.models.load_model(os.path.join(file_path, file_name))

class BlazeFace():
    def __init__(self):
        self.model = load_model()

    def detect(self, img):
        orig_h, orig_w = img.shape[0:2]
        frame = facedet_utils.create_letterbox_image(img, 128)
        h, w = frame.shape[0:2]
        input_frame = cv2.cvtColor(cv2.resize(frame, (128, 128)), cv2.COLOR_BGR2RGB)
        input_tensor = np.expand_dims(input_frame.astype(np.float32), 0) / 127.5 - 1
        result = self.model.predict(input_tensor, verbose=0)[0]
        final_boxes, landmarks_proposals = facedet_utils.process_detections(result, (orig_h, orig_w), 5, 0.75, 0.5, pad_ratio=0.5)
        if len(final_boxes) == 0:
            return [], ()
        keypoints = facedet_utils.get_keypoints(landmarks_proposals)
        faces = []
        regions = []
        for index in range(len(final_boxes)):
            bbox = final_boxes[index]
            keypoint = keypoints[index]
            face = img[bbox[1] : bbox[3], bbox[0] : bbox[2]]
            face = self.align(face, keypoint)
            faces.append(face)
            regions.append((bbox[0], bbox[2], bbox[1], bbox[2]))
        
        return faces, regions

    def align(self, img, keypoints):
        left_eye = keypoints['left_eye']
        right_eye = keypoints['right_eye']
        left_eye_x, left_eye_y = keypoints['left_eye']
        right_eye_x, right_eye_y = keypoints['right_eye']

        if left_eye_y > right_eye_y:
            point_3rd = (left_eye_x, right_eye_y)
            direction = 1 
        else:
            point_3rd = (right_eye_x, left_eye_y)
            direction = -1
        
        a = distance.findEuclideanDistance(np.array(left_eye), np.array(point_3rd))
        b = distance.findEuclideanDistance(np.array(right_eye), np.array(point_3rd))
        c = distance.findEuclideanDistance(np.array(right_eye), np.array(left_eye))

        if b != 0 and c != 0:
            cos_a = (b * b + c * c - a * a) / (2 * b * c)
            angle = np.arccos(cos_a)
            angle = (angle * 180) / math.pi
            if direction == -1:
                angle = 90 - angle

            img = Image.fromarray(img)
            img = np.array(img.rotate(direction * angle))
        
        return img