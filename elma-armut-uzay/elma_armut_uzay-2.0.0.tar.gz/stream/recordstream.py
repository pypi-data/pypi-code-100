import datetime
import time
from stream.Camera import Camera
import cv2
from timestamped import timestamped_frame

import numpy as np


def record_stream(source: str, limit: int, time_sleep: int, frame_rate: float, output_path: str):
    cap = Camera(source)
    counter = 0
    out = cv2.VideoWriter(
        output_path + str(datetime.datetime.now().strftime("%H-%M-%S")) + '.mp4',
        cv2.VideoWriter_fourcc(*'MP4V'),
        frame_rate,
        (2560, 1440)
    )
    while True:
        time.sleep(time_sleep)
        frame = cap.getFrame()
        counter += 1
        if frame is not None:
            out.write(timestamped_frame(frame))
            print('Recording frame' + str(counter) + '/' + str(limit))  # Debug
            if counter == limit:
                return out.release()
            continue
        else:
            # When connection is lost. This script will stopped. Then shell command run again.
            print('Connection Issue. Exiting script...')  # Debug
            time.sleep(5)
            return out.release()


if __name__ == "__main__":
    record_stream(
        source='',  # What is source link?
        limit=100,  # How many frames will be captured for this video.
        time_sleep=1,  # How many times have a frame in seconds?
        frame_rate=1.0,  # How many frames per second in the video?
        output_path='../storage/'
    )
