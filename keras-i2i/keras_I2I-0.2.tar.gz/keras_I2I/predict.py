from tensorflow.keras.models import load_model
from numpy import load
from numpy import vstack
from matplotlib import pyplot
from numpy.random import randint

def generate_images(model_path, img_array):
    model = load_model(model_path)
    gen_image = model.predict(img_array)

    return gen_image

