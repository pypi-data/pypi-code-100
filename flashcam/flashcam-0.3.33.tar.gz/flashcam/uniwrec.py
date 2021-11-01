#!/usr/bin/env python3

# import the necessary packages
from imutils.video import VideoStream
import socket
import time
import signal
from contextlib import contextmanager
import argparse

import cv2
import datetime
import time

import datetime as dt

import os


from fire import Fire
import imutils

import urllib.request
import numpy as np

# user pass
import  base64

import getpass

import sys

@contextmanager
def timeout(time):
    # register a function to raise a TimeoutError on the signal
    signal.signal(signal.SIGALRM, raise_timeout)
    # schedule the signal to be sent after 'time'
    signal.alarm(time)
    #print("D... timeout registerred")

    try:
        tok = False
        #print("D... yielding timeout")
        yield
    finally:
        tok = True
        # unregister the signal so it wont be triggered if the timtout is not reached
        #print("D... timeout NOT!  unregisterred")
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
    raise TimeoutError




def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

def img_estim(img, thrshld=127):
    res = np.mean(img)
    return res
    is_light =  res > thrshld
    return 'light' if is_light else 'dark'
    # 40 -> 2.2







def display2(videodev, save = False,
         passfile="~/.pycamfw_userpass"):
    """
    """

    def get_stream():
        # localuser
        u,p=getpass.getuser(),"a"
        try:
            with open( os.path.expanduser(passfile) ) as f:
                print("YES---> PASSWORD FILE  ", passfile )
                w1 = f.readlines()
                u= w1[0].strip()
                p= w1[1].strip()
        except:
            print("NO PASSWORD FILE  ", passfile)


        print("D... capturing from web:/{}/".format(videodev) )
        #cam = cv2.VideoCapture( videodev )
        #stream = urllib.request.urlopen( videodev )

        request = urllib.request.Request( videodev )
        print("D... USER/PASS", u,p)
        base64string =base64.b64encode( bytes(  '%s:%s' % (u, p ), 'ascii') )
        print("D... stream ok1", base64string)
        request.add_header("Authorization", "Basic %s" % base64string.decode('utf-8'))

        #request.add_header("Authorization", "Basic %s" % base64string)
        print("D... stream ok2 - request.urlopen (disp)")
        ok = False
        try:
            stream = urllib.request.urlopen(request, timeout=3)
            ok = True
            print("D... stream ok3")
        except:
            ok = False
            stream = None
            print("X.... Timeouted")


        return stream, u, p


    while True: #==================== MAIN LOOP =================

        mjpg =False

        rpiName = socket.gethostname()
        # #===================== OPENCV START CAPTURE==========================

        bytex = b'' # stream
        rpi_name = videodev

        if (str(videodev).find("http://")==0) or (str(videodev).find("https://")==0):
            # infinite loop for stream authentication
            stream = None
            while stream is None:
                print("D... waiting for stream")
                ### HERE PUT BWIMAGE
                #cv2.imshow(rpi_name, frame) # 1 window for each RPi
                if "frame" in locals():
                    print("D... frame in locals() ")
                    if (not frame is None):
                        print("D.... graying")
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                        (w, h, c) = frame.shape

                        for i in range(0,w,10):
                            x1, y1 = 0, i
                            x2, y2 = h, i
                            line_thickness = 1
                            cv2.line(gray, (x1, y1), (x2, y2), (111, 111, 111),
                                 thickness=line_thickness)
                        cv2.imshow(rpi_name, gray) # 1 window for each RPi
                        key = cv2.waitKey(1)

                time.sleep(1)
                stream, u, p  = get_stream()
        else:
            print("X... use http:// address")
            sys.exit(0)



        if (str(videodev).find("http://")==0) or (str(videodev).find("https://")==0):
            ret_val=0
            oi = 0
            while ret_val == 0:
                oi+=1
                bytex += stream.read(1024)
                a = bytex.find(b'\xff\xd8') #frame starting
                b = bytex.find(b'\xff\xd9') #frame ending
                if a != -1 and b != -1:
                    jpg = bytex[a:b+2]
                    bytex = bytex[b+2:]
                    # frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    ret_val= 1
                    print("D...                ok frame http",oi,len(bytex) )
                else:
                    ret_val = 0
                    print("D...          frame set None http",oi,len(bytex), end="\r")
                    #frame = None

#----------------------------------------------------------------

        sfilename = ""
        sfilenamea = ""
        if save:
            sname = "rec"
            sfilenamea = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            sme = socket.gethostname()
            sfilenamea = f"{sme}{sname}_{sfilenamea}.avi"
            sfilenamea = os.path.expanduser("~/" + sfilenamea)
            sfourcc = cv2.VideoWriter_fourcc(*'XVID')
            saviout = cv2.VideoWriter( sfilenamea,sfourcc,25.0, (640,480))
            print( sfilenamea )
            print( sfilenamea )
            print( sfilenamea )
            print( sfilenamea )


        first = True

        timestamp_of_last_socket_refresh = time.time()


        i = 0
        fps = 0
        resetfps = True
        lastminu = 88
        motion_last = "999999"

        i7 = 0
        artdelay=0.05

        connection_ok = True
        while connection_ok: #========================================================
            # read the frame from the camera and send it to the server
            #time.sleep(0.05)

            print("-", end="")
            #while True:
            if (str(videodev).find("http://")==0) or (str(videodev).find("https://")==0):
                artdelay = 0
                ret_val = 0
                try:
                    with timeout(2):
                        while ret_val == 0:
                            for i8 in range(1): # I decimate and remove delay
                                print("1-", flush=True,end="")
                                bytex += stream.read(1024*10)
                                a = bytex.find(b'\xff\xd8') #frame starting
                                b = bytex.find(b'\xff\xd9') #frame ending
                                if a != -1 and b != -1:
                                    jpg = bytex[a:b+2]
                                    bytex = bytex[b+2:]
                                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                                    ret_val=1
                                    print("got  Size={:6.0f}kB {} {}".format(
                                        len(bytex)/1024,
                                        datetime.datetime.now(),
                                        sfilenamea
                                    ) , end="\r")
                                else:
                                    ret_val = 0
                                    #frame = None
                                    print("Non  sizE={:6.0f}kB ".format(len(bytex)/1024), end = "\r" )
                except:
                    print("X... exception - connection lost, ")
                    ret_val = 0
                    #frame = None
                    print("RDE  siZe={:6.0f}kB ".format(len(bytex)/1024), end = "\n" )
                    connection_ok = False


                print("-2", flush=True,end="")

                #while


            if connection_ok:
                if (ret_val == 0) or (type(frame)=="NoneType"):
                    print("Not a good frame", type(frame), end="\r")
                    continue
                (w, h, c) = frame.shape
                frame_area = w*h
                motion_det = False
                print(".", end="")
                #print("RPINAME=",rpi_name)
                #print(frame)

                wname = videodev
                cv2.namedWindow( wname, cv2.WINDOW_KEEPRATIO)
                cv2.resizeWindow(wname, frame.shape[1], frame.shape[0] )

                cv2.imshow(rpi_name, frame) # 1 window for each RPi
                if save:
                    saviout.write(frame)

                # time.sleep(0.2)
                key = cv2.waitKey(1)

                if (not frame is None) and (rpi_name!="") and (key == ord('q')):
                    print("Q PRESSED!")
                    sys.exit(1)
                if (not frame is None) and (rpi_name!="") and (key == ord('s')):
                    print("S PRESSED!")
                    sname = "snapshot"
                    sfilename = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
                    sme = socket.gethostname()
                    sfilename = f"{sme}{sname}_{sfilename}.jpg"
                    sfilename = os.path.expanduser( "~/"+sfilename )
                    # sfourcc = cv2.VideoWriter_fourcc(*'XVID')
                    # saviout = cv2.VideoWriter( sfilename , sfourcc , 25.0, (640,480))
                    isWritten = cv2.imwrite( sfilename, frame )
                    if isWritten:
                        print('Image is successfully saved as file.', sfilename)





if __name__=="__main__":
    Fire( display2)
    #Fire({ "disp":display2,   "disp2":display2    })
