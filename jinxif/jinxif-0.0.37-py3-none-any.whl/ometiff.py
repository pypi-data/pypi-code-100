
import aicsimageio

from aicsimageio import AICSImage

class aicsimageio.writers.ome_tiff_writer.OmeTiffWriter[source]


import numpy as np
from aicsimageio.writers import OmeTiffWriter

image = np.random.rand(10, 3, 1024, 2048)
OmeTiffWriter.save(image, "file.ome.tif", dim_order="ZCYX")


