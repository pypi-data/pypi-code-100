import pandas as pd
import os
import requests
import io
import numpy as np
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt
from keras.applications import vgg19
from keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping
import keras.preprocessing.image as process_im
from tensorflow.python.keras import models 
from tensorflow.python.keras import losses
from tensorflow.python.keras import layers
from tensorflow.python.keras import backend as K
import functools
import IPython.display
import logging

logger = logging.getLogger(__name__)

CONTENT_LATERS = ['block5_conv2']
STYLE_LAYERS = ['block1_conv1', 'block2_conv1', 'block3_conv1', 'block4_conv1', 'block5_conv1']
N_CONTENT = len(CONTENT_LATERS)
N_STYLE = len(STYLE_LAYERS)

def load_file(image_path, path_type='local', max_dim=512):
    """
    This function is used to load the image from givn path
    input -> image path
    output -> numpy image array
    convert the image to RGB and resize it to the given dimension
    """
    if path_type=='local':
        image =  Image.open(image_path)
    elif path_type=='url':
        response = requests.get(image_path)
        image_bytes = io.BytesIO(response.content)
        image =  Image.open(image_bytes)
    else:
        print("Please enter valid path type")

    image = image.convert(mode='RGB')
    factor = max_dim/max(image.size)
    image = image.resize((round(image.size[0]*factor),round(image.size[1]*factor)),Image.ANTIALIAS)
    im_array = process_im.img_to_array(image)
    im_array = np.expand_dims(im_array,axis=0) #adding extra axis to the array as to generate a 
                                               #batch of single image 
    return im_array

def show_im(img, title=None):

    """
    Simple function to display the image from given image array
    """

    #squeeze array to drop batch axis
    img=np.squeeze(img, axis=0)
    plt.imshow(np.uint8(img))
    if title is None:
        pass
    else:
        plt.title(title)
    plt.imshow(np.uint8(img))

def get_content_loss(noise, target):
    loss = tf.reduce_mean(tf.square(noise-target))
    return loss

def get_style_loss(noise, target):
    gram_noise = gram_matrix(noise)
    loss = tf.reduce_mean(tf.square(target-gram_noise))
    return loss

def get_features(model, content_image, style_image):
    content_img = img_preprocess(content_image)
    style_image = img_preprocess(style_image)
    
    content_output = model(content_img)
    style_output = model(style_image)
    
    content_feature = [layer[0] for layer in content_output[N_STYLE:]]
    style_feature = [layer[0] for layer in style_output[:N_STYLE]]
    return content_feature, style_feature

def gram_matrix(tensor):
    channels = int(tensor.shape[-1])
    vector = tf.reshape(tensor,[-1,channels])
    n = tf.shape(vector)[0]
    gram_matrix = tf.matmul(vector, vector, transpose_a=True)
    return gram_matrix/tf.cast(n,tf.float32)

def img_preprocess(image):
    img = tf.keras.applications.vgg19.preprocess_input(image)
    return img

def deprocess_img(processed_img):

    x = processed_img.copy()
    if len(x.shape) == 4:
        x = np.squeeze(x, 0)
    assert len(x.shape) == 3 #Input dimension must be [1, height, width, channel] or [height, width, channel]


    # perform the inverse of the preprocessing step
    x[:, :, 0] += 103.939
    x[:, :, 1] += 116.779
    x[:, :, 2] += 123.68
    x = x[:, :, ::-1] # converting BGR to RGB channel

    x = np.clip(x, 0, 255).astype('uint8')
    return x

def compute_loss(model, loss_weights,image, gram_style_features, content_features):

    style_weight, content_weight = loss_weights #style weight and content weight are user given parameters
                                               #that define what percentage of content and/or style will be preserved in the generated image
    
    output = model(image)
    content_loss = 0
    style_loss = 0
    
    noise_style_features = output[:N_STYLE]
    noise_content_feature = output[N_STYLE:]
    
    weight_per_layer = 1.0/float(N_STYLE)
    for a,b in zip(gram_style_features,noise_style_features):
        style_loss+=weight_per_layer*get_style_loss(b[0],a)
        
    
    weight_per_layer =1.0/float(N_CONTENT)
    for a,b in zip(noise_content_feature,content_features):
        content_loss+=weight_per_layer*get_content_loss(a[0],b)
        
    style_loss *= style_weight
    content_loss *= content_weight
    total_loss = content_loss + style_loss
    
    return total_loss, style_loss, content_loss


def compute_grads(dictionary):

    with tf.GradientTape() as tape:
        all_loss=compute_loss(**dictionary)

    total_loss=all_loss[0]
    return tape.gradient(total_loss,dictionary['image']), all_loss


class Model():

    def __init__(self):
        logger.debug("Building model")

        vgg = tf.keras.applications.vgg19.VGG19(include_top=False,weights='imagenet')
        vgg.trainable=False
        content_output = [vgg.get_layer(layer).output for layer in CONTENT_LATERS]
        style_output = [vgg.get_layer(layer).output for layer in STYLE_LAYERS]
        model_output = style_output + content_output
        self.model = models.Model(vgg.input,model_output)

        for layer in self.model.layers:
            layer.trainable = False
        print("model build is done")
    
    def setContentImage(self, path, path_type):
        self.ContentImage = load_file(path, path_type)

    def setStyleImage(self, path, path_type):
        self.StyleImage = load_file(path, path_type)

    def showContentImage(self):
        return show_im(self.ContentImage)
    
    def showStyleImage(self):
        return show_im(self.setStyleImage)

    def train(self, contentWeight=1e3, styleWeight=1e-2, epochs=500):
        
        contentFeatures, styleFeatures = get_features(self.model, self.ContentImage, self.StyleImage)     
        styleGrams = [gram_matrix(feature) for feature in styleFeatures]
        optimizer = tf.keras.optimizers.Adam(learning_rate=5, beta_1=0.99, epsilon=1e-1)
        best_loss,best_img = float('inf'), None
        noise = img_preprocess(self.ContentImage)
        noise = tf.Variable(noise, dtype=tf.float32)
        
        loss_weights = (styleWeight, contentWeight)
        dictionary = {
                    'model': self.model,
                    'loss_weights': loss_weights,
                    'image': noise,
                    'gram_style_features': styleGrams,
                    'content_features': contentFeatures
                    }
        
        norm_means = np.array([103.939, 116.779, 123.68])
        min_vals = -norm_means
        max_vals = 255 - norm_means   
    
        imgs = []
        for i in range(epochs):
            grad, all_loss = compute_grads(dictionary)
            total_loss, style_loss, content_loss = all_loss
            optimizer.apply_gradients([(grad,noise)])
            clipped = tf.clip_by_value(noise, min_vals, max_vals)
            noise.assign(clipped)
            
            if total_loss<best_loss:
                best_loss = total_loss
                best_img = deprocess_img(noise.numpy())
                
                print('Epoch: {}'.format(i))
                print('Total loss: {}, ' 
                            'style loss: {}, '
                            'content loss: {}, '.format(total_loss, style_loss, content_loss))
        print("Training Completed")

        target = Image.fromarray(best_img)
        return target