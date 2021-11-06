import tempfile

import numpy as np
import pytest

from handypy import hcv2 as cv2


def test_putText():
    img = np.zeros((256, 256, 3), np.uint8)
    cv2.putText(img, "msg")

    img = np.zeros((256, 256), np.uint8)
    cv2.putText(img, "msg")


def test_put_chinese_text():
    img = np.zeros((256, 256, 3), np.uint8)
    cv2.putChineseText(img, "中文", bottomLeftOrigin=True, thickness=2, lineType=0)

    img = np.zeros((256, 256), np.uint8)
    cv2.putChineseText(img, "中文")

    with pytest.raises(OSError):
        cv2.putChineseText(img, "中文", font="unknown")


def test_im_read_write():
    with tempfile.TemporaryDirectory() as f:
        tmp = f + "/test.png"
        img = np.zeros((256, 256, 3), np.uint8)
        cv2.imwrite(tmp, img)
        cv2.imwrite(img, tmp)
        cv2.imwrite(tmp, img=img)
        cv2.imwrite(img=img, filename=tmp)

        img2 = cv2.imread(tmp)
        assert (img == img2).all(), "Img io problem"

    with pytest.raises(FileNotFoundError):
        cv2.imread(tmp)

    with pytest.raises(RuntimeError):
        cv2.imwrite(tmp, img)
