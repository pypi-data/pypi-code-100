from cv2 import cv2
import datetime
import time

# From utils
from stream.Camera import Camera
from stream.timestamped import timestamped
from stream.info import shape


def record(
        # Function args.
        RTSP_URL: str,
        output_path: str,
        add_time_stamped: bool,
        frame_rate: float,
        time_sleep: float
):
    """
    :param RTSP_URL:
    :param output_path:
    :param add_time_stamped:
    :param frame_rate:
    :param time_sleep:
    :return:
    """
    # Add comment
    cap = Camera(RTSP_URL)

    # Add comment
    video = cv2.VideoWriter(
        output_path + str(datetime.datetime.now().strftime("%H-%M-%S")) + '.mp4',
        cv2.VideoWriter_fourcc(*'MP4V'),
        frame_rate,
        (shape(RTSP_URL))
    )
    print('Stream recording started.')
    # Add comment
    while True:
        time.sleep(time_sleep)  # Add comment
        frame = cap.getFrame()
        if frame is not None:
            print('Stream is recording...')  # Debug
            video.write(timestamped(add_time_stamped, frame))
        else:
            # When connection is lost. This script will stopped. Then shell command run again.
            print('Connection Issue. Exiting script...')  # Debug
            time.sleep(5)
            return video.release()


if __name__ == "__main__":
    record(
        RTSP_URL='',
        output_path='',
        frame_rate=15.0,
        time_sleep=1.0,
        add_time_stamped=True
    )
