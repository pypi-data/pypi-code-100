"""
Handy CV2
=========

"""
import logging

import cv2 as _cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

logger = logging.getLogger(__name__)


def putText(image: np.ndarray, text: str,
            org=(0, 0),
            font=_cv2.FONT_HERSHEY_PLAIN,
            fontScale=1, color=(0, 0, 255),
            thickness=1,
            lineType=_cv2.LINE_AA,
            bottomLeftOrigin=False) -> np.ndarray:
    """Add text to `cv2` image, with default values.

    :param image: image array
    :param text: text to be added
    :param org: origin of text, from top left by default
    :param font: font choice
    :param fontScale: font size
    :param color: BGR color, red by default
    :param thickness: font thickness
    :param lineType: line type of text
    :param bottomLeftOrigin: True to start from bottom left, default False
    :return: image with text added
    """
    return _cv2.putText(image, text, org, font, fontScale, color, thickness, lineType, bottomLeftOrigin)


def putChineseText(image: np.ndarray, text: str,
                   org=(0, 0),
                   font=None,
                   fontScale=1, color=(0, 0, 255),
                   thickness=1,
                   lineType=None,
                   bottomLeftOrigin=False) -> np.ndarray:
    """Add CJK text to image

    :param image: image array
    :param text: text to be added
    :param org: origin of text, from top left by default
    :param font: font name if in the system, or font file path
    :param fontScale: font size. Size 1 corresponds to 12 pixel.
    :param color: BGR color, default red.
    :param thickness: no effect, place holder.
    :param lineType:  no effect, place holder.
    :param bottomLeftOrigin: True to start from bottom left, default False
    :return: image with text added
    """
    grey_flag = len(image.shape) == 2
    if grey_flag:
        image = _cv2.cvtColor(image, _cv2.COLOR_GRAY2BGR)

    if bottomLeftOrigin:
        org = list(org)
        org[1] = image.shape[1] - org[1]

    fontScale = int(fontScale * 12)

    if thickness != 1:
        logger.warning("`thickness` is not in-use. Use fontScale to control thickness.")
    if lineType is not None:
        logger.warning("`lineType` is not in-use. Use font to control style.")

    try:
        if font is None:
            try:
                import importlib.resources as pkg_resources
            except ImportError:
                # Try backported to PY<37 `importlib_resources`.
                import importlib_resources as pkg_resources
            from . import resources
            with pkg_resources.path(resources, 'NotoSansCJK-Bold.ttc') as p:
                font = ImageFont.truetype(str(p), fontScale)
        else:
            font = ImageFont.truetype(font, fontScale)
    except OSError as e:
        logger.fatal("Download missing font %s" % font)
        raise e

    img_PIL = Image.fromarray(image)
    draw = ImageDraw.Draw(img_PIL)
    draw.text(org, text, font=font, fill=color[::-1], )
    image = np.asarray(img_PIL)
    if grey_flag:
        image = _cv2.cvtColor(image, _cv2.COLOR_BGR2GRAY)
    return image


def imread(*args, **kwargs) -> np.ndarray:
    """Fail-safe image read

    :param args: Pass to :code:`cv2.imread()`.  `filename` is required.
    :param kwargs: Pass to :code:`cv2.imread()`.
    :return: image numpy array
    """
    img = _cv2.imread(*args, **kwargs)
    if img is None:
        raise FileNotFoundError(args[0])
    return img


def imwrite(*args, **kwargs) -> int:
    """Fail-safe and convenient image write.  Put image and image filename in any order.

    :param args: Pass to :code:`cv2.imwrite()`.  `filename` and `img` are required as arguments (order-free) or keywords.
    :param kwargs: Pass to :code:`cv2.imwrite()`.
    :return: 0,1
    :raise: RuntimeError
    """
    if 'filename' not in kwargs and 'img' not in kwargs:
        if isinstance(args[1], str):
            args = [i for i in args]
            args[0], args[1] = args[1], args[0]
    flag = _cv2.imwrite(*args, **kwargs)

    if flag == 0:
        raise RuntimeError("Fail to write to %s" % args[0])
    return flag

# TODO: ratio-based resize functions
