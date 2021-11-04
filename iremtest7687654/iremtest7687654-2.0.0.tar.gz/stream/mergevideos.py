import os
import cv2
import datetime


def merge_videos(listdir_path:str, file_endswith:str, frame_rate:float):
    # Merge multiple videos
    # Define output video variables first
    out = cv2.VideoWriter(
        str(listdir_path + datetime.datetime.now().strftime("%H-%M-%S")) + '__merged__' + '.mp4',
        cv2.VideoWriter_fourcc(*'MP4V'),
        frame_rate, # Frame rate of the new video
        (2560, 1440) # w,h value of the video
    )
    # List files in folder.
    for file in sorted(os.listdir(listdir_path)):
        # Get only mp4 files
        if file.endswith(file_endswith):
            print('File merging :' + file)
            cap = cv2.VideoCapture(listdir_path + file)
            while True:
                ret, frame = cap.read()
                if ret is True:
                    out.write(frame)
                else:
                    print(file + ' added.')
                    break


if __name__ == "__main__":
    merge_videos(
        listdir_path='../storage/',
        file_endswith='.mp4',
        frame_rate=15.0
    )
