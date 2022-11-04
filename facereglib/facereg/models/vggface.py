from keras.models import Model, Sequential
from keras.layers import Convolution2D, ZeroPadding2D, MaxPooling2D, Flatten, Dropout, Activation
import os
import gdown

def load_model():
    base_model = Sequential()

    base_model.add(ZeroPadding2D((1,1),input_shape=(224,224, 3)))
    base_model.add(Convolution2D(64, (3, 3), activation='relu'))
    base_model.add(ZeroPadding2D((1,1)))
    base_model.add(Convolution2D(64, (3, 3), activation='relu'))
    base_model.add(MaxPooling2D((2,2), strides=(2,2)))

    base_model.add(ZeroPadding2D((1,1)))
    base_model.add(Convolution2D(128, (3, 3), activation='relu'))
    base_model.add(ZeroPadding2D((1,1)))
    base_model.add(Convolution2D(128, (3, 3), activation='relu'))
    base_model.add(MaxPooling2D((2,2), strides=(2,2)))

    base_model.add(ZeroPadding2D((1,1)))
    base_model.add(Convolution2D(256, (3, 3), activation='relu'))
    base_model.add(ZeroPadding2D((1,1)))
    base_model.add(Convolution2D(256, (3, 3), activation='relu'))
    base_model.add(ZeroPadding2D((1,1)))
    base_model.add(Convolution2D(256, (3, 3), activation='relu'))
    base_model.add(MaxPooling2D((2,2), strides=(2,2)))

    base_model.add(ZeroPadding2D((1,1)))
    base_model.add(Convolution2D(512, (3, 3), activation='relu'))
    base_model.add(ZeroPadding2D((1,1)))
    base_model.add(Convolution2D(512, (3, 3), activation='relu'))
    base_model.add(ZeroPadding2D((1,1)))
    base_model.add(Convolution2D(512, (3, 3), activation='relu'))
    base_model.add(MaxPooling2D((2,2), strides=(2,2)))

    base_model.add(ZeroPadding2D((1,1)))
    base_model.add(Convolution2D(512, (3, 3), activation='relu'))
    base_model.add(ZeroPadding2D((1,1)))
    base_model.add(Convolution2D(512, (3, 3), activation='relu'))
    base_model.add(ZeroPadding2D((1,1)))
    base_model.add(Convolution2D(512, (3, 3), activation='relu'))
    base_model.add(MaxPooling2D((2,2), strides=(2,2)))

    base_model.add(Convolution2D(4096, (7, 7), activation='relu'))
    base_model.add(Dropout(0.5))
    base_model.add(Convolution2D(4096, (1, 1), activation='relu'))
    base_model.add(Dropout(0.5))
    base_model.add(Convolution2D(2622, (1, 1)))
    base_model.add(Flatten())
    base_model.add(Activation('softmax'))

    file_path = os.getcwd() + '/facereglib/facereg/weights/'
    file_name = 'vgg_face_weights.h5'
    if not os.path.exists(file_path + file_name):
        os.makedirs(file_path, exist_ok=True)
        id = '1UPvEypf7xiY5mOAn1qJwWj2mItTpdHVx'
        gdown.download(id=id, output=file_path + file_name, quiet=False)
    base_model.load_weights(file_path + file_name)

    vggface_model = Model(inputs=base_model.layers[0].input, outputs=base_model.layers[-2].output)

    return vggface_model