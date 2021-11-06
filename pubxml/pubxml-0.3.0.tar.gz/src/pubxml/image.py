
# * Keys are mode values returned by PIL.Image.mode
# * Descriptions are from 
#   https://pillow.readthedocs.io/en/3.1.x/handbook/concepts.html#concept-modes

IMAGE_MODES = {
    '1': '1-bit pixels, black and white, stored with one pixel per byte',
    'L': '8-bit pixels, black and white',
    'P': '8-bit pixels, mapped to any other mode using a color palette',
    'RGB': '3x8-bit pixels, true color',
    'RGBA': '4x8-bit pixels, true color with transparency mask',
    'CMYK': '4x8-bit pixels, color separation',
    'YCbCr': '3x8-bit pixels, color video format',
    'LAB': '3x8-bit pixels, the L*a*b color space',
    'HSV': '3x8-bit pixels, Hue, Saturation, Value color space',
    'I': '32-bit signed integer pixels',
    'F': '32-bit floating point pixels',
    'LA': '(8-bit pixels, black and white with alpha',
    'RGBX': 'true color with padding)',
    'RGBa': 'true color with premultiplied alpha',
}

