import datetime
import numpy
from cv2 import cv2


def timestamped(add_stamped: bool, frame: numpy.ndarray):
    if add_stamped is True:
        location = ((2560 - 600), (1440 - 100))  # From actual shape size.
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (0, 0, 255)
        thickness = 2
        return cv2.putText(
            frame,
            str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            location,
            font,
            fontScale,
            color,
            thickness,
            cv2.LINE_AA,
            False
        )
    else:
        return frame


if __name__ == "__main__":
    # Example Numpy Array
    w, h = 512, 512
    data = numpy.zeros((h, w, 3), dtype=numpy.uint8)
    data[0:256, 0:256] = [255, 0, 0]  # red patch in upper left

    timestamped(
        add_stamped=True,
        frame=data
    )
