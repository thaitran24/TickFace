from keras.models import Model, Sequential
from keras.layers import Convolution2D, LocallyConnected2D, MaxPooling2D, Flatten, Dense, Dropout
import os
import gdown

def load_model():
    base_model = Sequential()

    base_model.add(Convolution2D(32, (11, 11), activation='relu', name='C1', input_shape=(152, 152, 3)))
    base_model.add(MaxPooling2D(pool_size=3, strides=2, padding='same', name='M2'))
    base_model.add(Convolution2D(16, (9, 9), activation='relu', name='C3'))
    base_model.add(LocallyConnected2D(16, (9, 9), activation='relu', name='L4'))
    base_model.add(LocallyConnected2D(16, (7, 7), strides=2, activation='relu', name='L5') )
    base_model.add(LocallyConnected2D(16, (5, 5), activation='relu', name='L6'))
    base_model.add(Flatten(name='F0'))
    base_model.add(Dense(4096, activation='relu', name='F7'))
    base_model.add(Dropout(rate=0.5, name='D0'))
    base_model.add(Dense(8631, activation='softmax', name='F8'))

    file_path = os.getcwd() + '/facereglib/facereg/weights/'
    file_name = 'vgg_face_weights.h5'
    if not os.path.exists(file_path + file_name):
        os.makedirs(file_path, exist_ok=True)
        id = '1vnh49m00u1C8vGegYVEN2XJ40XzPfwYD'
        gdown.download(id=id, output=file_path + file_name, quiet=False)
    base_model.load_weights(file_path + file_name)

    deepface_model = Model(inputs=base_model.layers[0].input, outputs=base_model.layers[-3].output)

    return deepface_model

