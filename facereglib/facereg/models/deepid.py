from keras.models import Model
from keras.layers import Conv2D, Activation, Input, Add, MaxPooling2D, Flatten, Dense, Dropout
import os
import gdown

def loadModel():
    input = Input(shape=(55, 47, 3))

    x = Conv2D(20, (4, 4), name='Conv1', activation='relu', input_shape=(55, 47, 3))(input)
    x = MaxPooling2D(pool_size=2, strides=2, name='Pool1')(x)
    x = Dropout(rate=0.99, name='D1')(x)

    x = Conv2D(40, (3, 3), name='Conv2', activation='relu')(x)
    x = MaxPooling2D(pool_size=2, strides=2, name='Pool2')(x)
    x = Dropout(rate=0.99, name='D2')(x)

    x = Conv2D(60, (3, 3), name='Conv3', activation='relu')(x)
    x = MaxPooling2D(pool_size=2, strides=2, name='Pool3')(x)
    x = Dropout(rate=0.99, name='D3')(x)

    x1 = Flatten()(x)
    fc11 = Dense(160, name = 'fc11')(x1)

    x2 = Conv2D(80, (2, 2), name='Conv4', activation='relu')(x)
    x2 = Flatten()(x2)
    fc12 = Dense(160, name = 'fc12')(x2)

    y = Add()([fc11, fc12])
    y = Activation('relu', name = 'deepid')(y)

    deepid_model = Model(inputs=[input], outputs=y)

    file_path = os.getcwd() + '/facereglib/facereg/weights/'
    file_name = 'deepid_keras_weights.h5'
    if not os.path.exists(file_path + file_name):
        os.makedirs(file_path, exist_ok=True)
        id = '1WW6Bxq_BQvgDNt0_q5b4LDILPssiylgU'
        gdown.download(id=id, output=file_path + file_name, quiet=False)
    deepid_model.load_weights(file_path + file_name)

    return deepid_model