import keras
import keras.layers as L

def build_autoencoder(img_shape, code_size):
    encoder = keras.models.Sequential()
    encoder.add(L.InputLayer(img_shape))
    encoder.add(L.Conv2D(32, (3, 3), strides=(1, 1), padding="same", use_bias=True))
    encoder.add(L.MaxPooling2D((2, 2)))
    encoder.add(L.Conv2D(256, (3, 3), strides=(1, 1), padding="same", use_bias=True))
    encoder.add(L.MaxPooling2D((2, 2)))
    encoder.add(L.Flatten())
    encoder.add(L.Dense(code_size))

    decoder = keras.models.Sequential()
    decoder.add(L.InputLayer((code_size,)))
    decoder.add(L.Dense(2 * 2 * 256))
    decoder.add(L.Reshape((2, 2, 256)))
    decoder.add(L.UpSampling2D((2, 2)))
    decoder.add(L.Conv2D(32, (3, 3), padding="same"))
    decoder.add(L.UpSampling2D((2, 2)))
    decoder.add(L.Conv2D(32, (3, 3), padding="same"))
    decoder.add(L.UpSampling2D((2, 2)))
    decoder.add(L.Conv2D(64, (3, 3), padding="same"))
    decoder.add(L.UpSampling2D((2, 2)))
    decoder.add(L.Conv2D(128, (3, 3), padding="same"))
    decoder.add(L.UpSampling2D((2, 2)))
    decoder.add(L.Conv2D(256, (3, 3), padding="same"))
    decoder.add(L.UpSampling2D((2, 2)))
    decoder.add(L.Conv2D(3, (3, 3), padding="same", activation=None))
    print(encoder.summary())
    print(decoder.summary())
    return encoder, decoder
