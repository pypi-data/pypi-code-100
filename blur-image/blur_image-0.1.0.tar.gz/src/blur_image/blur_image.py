
from PIL import Image, ImageFilter

def blur(source, output, mode="simple", value=None):
    original_image = Image.open(source)

    if mode == "simple":
        new_image = original_image.filter(ImageFilter.BLUR)
    elif mode == "box":
        new_image = original_image.filter(ImageFilter.BoxBlur(value))
    elif mode == "gaussian":
        new_image = original_image.filter(ImageFilter.GaussianBlur(5))       

    new_image.save(output)