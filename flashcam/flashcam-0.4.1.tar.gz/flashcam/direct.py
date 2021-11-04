#!/usr/bin/env python3


'''
This is screen interface
'''

from flashcam.version import __version__
from fire import Fire
from flashcam import config
from flashcam.real_camera import Camera

import time

import datetime as dt
import numpy as np

import cv2

import sys

# here is the config and camera TOO
import flashcam.web
# runs camera = Camera()
#from flashcam.web import camera_ins



def show_cam():
    #print(camera_ins)
    #global camera
    #print(camera)
    """
    vidnum = number; res 640x480;
    recommended= ... uses the recommend_video to restart the same cam
    """

    # print(f"i...  target_frame = {target_frame}, average={average}, blur={blur}")
    camera = Camera( ) # creating the OBJECT
    #print("direct = camera", camera, "  (web)camera",camera_ins)

    framecnt = 0
    framecnttrue = 0
    ss_time = 0
    wname = "placeholder"
    while True:
        time.sleep(0.1)
        framecnt+=1
        print("D... get_frame (gen)")
        frame = camera.get_frame()
        print("D... got_frame (gen)")
        start = dt.datetime.now()
        blackframe = np.zeros((480,640,3), np.uint8)

        #----- i dont send None now, but this helped to avoid crash
        if (frame is None):
            # frame=cv2.imencode('.jpg', frame)[1].tobytes()
        #else:
            continue
        stop = dt.datetime.now()
        ss_time = (stop-start).total_seconds()


        cv2.namedWindow( wname, cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow(wname, frame.shape[1], frame.shape[0] )

        cv2.imshow( wname , frame );
        k = cv2.waitKey(1)
        print("D... camera kill == ", camera.kill )
        if k == ord("q"):
            print("X... kill set to True")
            camera.killme()
            return
            #sys.exit(0)

        #===== MAYBE THIS IS WASTING - it should throw get_frame
        #  but with -k sync   it restarts

        ## yield ( frame)  #--------- JPEG vs MJPEG
        #yield (b'--frame\r\n' # ---- JPEG
        #       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')




def main():
    print("D... screen view")
    show_cam()

if __name__ == '__main__':
    print("i... APP RUN FROM direct.py")

    Fire(main)
