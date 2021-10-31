import cv
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import exposure

hog_ardi = cv.HOG()
hog_ardi.load_image('dataset_test/run.jpg')

#image = hog.create_zero_padding(hog.original_image)
#plt.imshow(image, cmap='gray')
#plt.show()

mag, hog_features = hog_ardi.extract_features()

plt.imshow(mag, cmap='gray')
plt.show()

print(np.min(hog_features))
print(np.max(hog_features))

hogfv, hog_image = hog(hog_ardi.original_image, orientations=9, pixels_per_cell=(8,8), 
                       cells_per_block=(2,2), visualize=True, multichannel=False)

hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0,1))
plt.imshow(hog_image_rescaled, cmap='gray')
plt.show()

print(np.min(hogfv))
print(np.max(hogfv))






'''
plt.imshow(hog.horizontal_derivative, cmap='gray')
plt.show()

plt.imshow(hog.vertical_derivative, cmap='gray')
plt.show()

plt.imshow(hog.edge_magnitude, cmap='gray')
plt.show()

plt.imshow(hog.edge_direction, cmap='gray')
plt.show()
'''
