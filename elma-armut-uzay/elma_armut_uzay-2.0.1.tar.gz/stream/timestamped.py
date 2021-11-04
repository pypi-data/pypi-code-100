import datetime
import cv2


def timestamped_frame(frame):
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
