import pkg_resources
import pylab as plt


def show_image():
    stream = pkg_resources.resource_stream(__name__, 'data/images/logo.jpg')
    image = plt.imread(stream)
    stream.close()
    plt.imshow(image)
    plt.show()
