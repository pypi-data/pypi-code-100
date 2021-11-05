#!/usr/bin/env python
# -*- coding: utf-8 -*-
from napari_plugin_engine import napari_hook_implementation
import numpy as np
import pdf2image
import os

@napari_hook_implementation
def napari_get_reader(path):
    if isinstance(path, str) and path.endswith(".pdf"):
      return pdf_reader


def pdf_reader(path: str):
    #TODO: Add PDF as pyramidal file
    pil_images = pdf2image.convert_from_path(path,
                                             dpi=300)
    images = [np.array(pil_image) for pil_image in pil_images]
    # Return all pages in one layer if shape same otherwise return individual layers
    shape = [im.shape for im in images]
    if all(x == shape[0] for x in shape):
        array = np.squeeze(np.stack(images))
        return [(array,)]
    else:
        # Ensure top layer is first page
        return [(im,) for im in images[::-1]]
