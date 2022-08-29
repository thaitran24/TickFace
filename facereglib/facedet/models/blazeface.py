import os
import gdown
from keras.models import load_model

def loadModel():
    file_path = os.getcwd() + '/facereglib/facedet/weights/'
    file_name = 'blazeface_tf.h5'
    if not os.path.exists(file_path + file_name):
        os.makedirs(file_path, exist_ok=True)
        id = '10REys3sjGpAW8fpLBDc65UxoWeJvE2ye'
        gdown.download(id=id, output=file_path + file_name, quiet=False)
    return load_model(file_path + file_name)