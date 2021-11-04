import time

from cv2 import cv2


# Add learn frame shape for cv2.VideoWriter etc...
def shape(RTSP_URL: str):
    print('Trying to get shape information...')
    cap = cv2.VideoCapture(RTSP_URL)
    if cap.isOpened():
        print('Shape information added')
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return w, h
    else:
        print("Couldn't get video frame information. Exiting the function...")
        time.sleep(3)
        return None


if __name__ == "__main__":
    print(shape(''))
