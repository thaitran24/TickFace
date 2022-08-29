from facereglib.facereg.models.facenet import InceptionResNetV2
import os
import gdown

def loadModel():
    facenet_model = InceptionResNetV2(dimension=512)

    file_path = os.getcwd() + '/facereglib/facereg/weights/'
    file_name = 'facenet512_weights.h5'
    if not os.path.exists(file_path + file_name):
        os.makedirs(file_path, exist_ok=True)
        id = '1gsT14J7T_oCgcuQ72COnjnZAqbYKjddf'
        gdown.download(id=id, output=file_path + file_name, quiet=False)
    facenet_model.load_weights(file_path + file_name)

    return facenet_model