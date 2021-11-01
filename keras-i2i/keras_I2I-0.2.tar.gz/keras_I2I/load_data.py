from os import listdir
from numpy import asarray
from numpy import vstack
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from numpy import savez_compressed

# load all images in a directory into memory
def load_images(path, lp, size):
	src_list = list()
	# enumerate filenames in directory, assume all are images
	for filename in lp:
		# load and resize the image
		pixels = load_img(path + '/' + filename, target_size=size)
		# convert to numpy array
		pixels = img_to_array(pixels) 
		# split into satellite and map
		img = pixels
		src_list.append(img)
	return asarray(src_list), size