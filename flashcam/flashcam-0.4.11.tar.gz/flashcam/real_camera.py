import cv2
from flashcam.base_camera2 import BaseCamera

from flashcam.usbcheck import recommend_video
# import base_camera  #  Switches: slowrate....

import datetime
import time
import socket

import glob

import subprocess as sp
import numpy as np

import flashcam.config as config

from  flashcam.stream_enhancer import Stream_Enhancer


from flashcam import v4lc

from flashcam.mmapwr import mmread_n_clear




# -----------------------------------------------------------------

# -----------------------------------------------------------------

class Camera(BaseCamera):
    video_source = 0

    @staticmethod
    def init_cam(  ):
        """
        should return videocapture device
        but also sould set Camerare.video_source
        """

        # ----------------------------
        #    we need to get in into the thread.....
        #  NOT NOW - all is taken from BaseCam
        # def __init__(self, target_frame = "direct" , average = 0, blur = 0 , threshold = 0):


        # res = "640x480"
        res = config.CONFIG["resolution"]
        print("D... init_cam caleld with:", res )
        print("i... init_cam caleld with:", res )


        vids = recommend_video( config.CONFIG["recommended"]  )
        if len(vids)>0:
            vidnum = vids[0]
            cap = cv2.VideoCapture(vidnum,  cv2.CAP_V4L2)

            # config.CONFIG["camera_on"] = True

            # - with C270 - it showed corrupt jpeg
            # - it allowed to use try: except: and not stuck@!!!
            #cap = cv2.VideoCapture(vidnum)
            #   70% stucks even with timeout
            pixelformat = "MJPG"
            w,h =  int(res.split("x")[0]), int(res.split("x")[1])
            fourcc = cv2.VideoWriter_fourcc(*pixelformat)
            cap.set(cv2.CAP_PROP_FOURCC, fourcc)
            cap.set(cv2
                    .CAP_PROP_FRAME_WIDTH,   w )
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT,  h )
            return cap,vidnum
        return None, None


    @staticmethod
    def frames( ):
        """
        recommended= ... uses the recommend_video to restart the same cam
        """
        # i need these to be in globals() ----evaluate from web.py
        global substract_background,save_background
        global speedx, speedy, restart_translate, average
        global gamma_divide, gamma_multiply,gamma_setdef,gain_divide,gain_multiply,gain_setdef

        # print("i... staticmethod frames @ real -  enterred; target_frame==", target_frame)
        senh = Stream_Enhancer()

        # -----------get parameters for DetMot, same for web as for all
        target_frame = config.CONFIG['target_frame']
        average      = int(config.CONFIG['average'])
        threshold    = int(config.CONFIG['threshold'])
        blur         = int(config.CONFIG['blur'])
        timelaps     = int(config.CONFIG['timelaps'])
        histogram    = config.CONFIG['histogram']
        res          = config.CONFIG['resolution']
        speedx          = float(config.CONFIG['x'])
        speedy          = float(config.CONFIG['y'])

        # ------------------    to evaluate commands from web.py
        substract_background = False
        save_background = False
        restart_translate = False
        gamma_divide = False
        gamma_multiply =False
        gamma_setdef =False
        gain_divide = False
        gain_multiply =False
        gain_setdef =False

        camera = Camera(  )
        cap, vidnum = camera.init_cam(  )

        cc = v4lc.V4L2_CTL("/dev/video"+str(vidnum))
        capa = cc.get_capbilities()


        # very stupid camera    ZC0303 Webcam
        if "exposure" in capa:
            exposure = cc.get_exposure()
            exposuredef = cc.getdef_exposure()
            print(f"i... EXPOAUTO == {exposure} vs def={exposuredef}; ")


        if "exposure_auto" in capa:
            expo_auto = cc.get_exposure_auto()
            expo_autodef = cc.getdef_exposure_auto()
            print(f"i... EXPOAUTO == {expo_auto} vs def={expo_autodef}; ")

        if "exposure_absolute" in capa:
            exposure_absolute = cc.get_exposure_absolute()

        if "gain" in capa:
            gain = cc.get_gain()
            gaindef = cc.getdef_gain()
        if "gamma" in capa:
            gamma = cc.get_gamma()
            gammadef = cc.getdef_gamma()


        nfrm = 0
        if config.CONFIG["recommended"]:
            wname = "none "
        else:
            wname = config.CONFIG["recommended"]


        frame_prev = None
        while True:


            timeoutok = False
            ret = False
            frame = None
            if (cap is None) or (not cap.isOpened()):
                print("X... camera None or not Opened(real)")
                ret = False
            else:
                try: #----this catches errors of libjpeg with cv2.CAP_V4L2
                    print(f"i... frame {nfrm:8d}   ", end="\r" )
                    ret, frame = cap.read()
                    BaseCamera.nframes+=1

                    #wname = f"res {frame.shape[1]}x{frame.shape[0]}"
                    nfrm+=1
                    #print(f"D... got frame (frames iter)   ret={ret}  {frame.shape}")
                except Exception as ex:
                    print("D... SOME OTHER EXCEPTION ON RECV...", ex)
                    config.CONFIG["camera_on"] = False


            if not ret:
                time.sleep(0.5)
                #vids = recommend_video(recommended) # try to re-init the same video
                #if len(vids)>0:
                #    vidnum = vids[0]
                config.CONFIG["camera_on"] = False

                cap = Camera.init_cam( )
                nfrm = 0

                # create gray + moving lines BUT prev_frame is bad sometimes
                try:
                    print("D... trying to gray frame")
                    frame = cv2.cvtColor(frame_prev, cv2.COLOR_BGR2GRAY)
                    height, width = frame.shape[0] , frame.shape[1]

                    skip = 10
                    startl = 2*(nfrm % skip) # moving lines
                    for il in range(startl,height,skip):
                        x1, y1 = 0, il
                        x2, y2 = width, il
                        #image = np.ones((height, width)) * 255
                        line_thickness = 1
                        cv2.line(frame, (x1, y1), (x2, y2), (111, 111, 111),
                                 thickness=line_thickness)
                except:
                    print("X... prev_frame was bad, no gray image")

            #print("D... ret==", ret)
            if ret: #********************************************************* operations
                frame_prev = frame
                if senh.add_frame(frame):  # it is a proper image....


                    #------------------------------ BRUTAL ------------test exposure V4L
                    if (BaseCamera.nframes % 10==0):
                        cc = v4lc.V4L2_CTL("/dev/video"+str(vidnum))
                        capa = cc.get_capbilities()
                        #cc.refresh()
                        exposure_absolute = 100
                        expo_auto = 3
                        expo_autodef = 3


                        # very stupid camera    ZC0303 Webcam - parallel to exposure_auto
                        if "exposure" in capa:
                            exposure = cc.get_exposure()

                        if "exposure_auto" in capa:  # if not auto, always tell _absolute
                            expo_auto = cc.get_exposure_auto()
                            expo_autodef = cc.getdef_exposure_auto()
                            print(f"i... EXPOAUTO == {expo_auto} vs def={expo_autodef}; ")

                        if "exposure_absolute" in capa:
                            exposure_absolute = cc.get_exposure_absolute()


                        if "gain" in capa:
                            gain = cc.get_gain()
                            gaindef = cc.getdef_gain()
                        if "gamma" in capa:
                            gamma = cc.get_gamma()
                            gammadef = cc.getdef_gamma()
                    #--------------------------------------------------------------------------




                    # ----------  I need to calculate histogram before labels...
                    if histogram: # just calculate a number on plain frame
                        hmean = senh.histo_mean( )

                    # ---------- before anything - we decode the web command
                    expression,value = mmread_n_clear( )
                    #print(f"i... expression == {expression}  value == {value}")
                    globals()[expression] = eval(value)
                    # print(".... substract_background", substract_background, not(substract_background) )
                    # globals()["substract_background"] = value

                    if save_background:
                        print("D... HERE I SAVE save_background of mask")
                        print("D... HERE I SAVE save_background of mask")
                        print("D... HERE I SAVE save_background of mask")
                        senh.save_background()
                        save_background = False  # ONE SHOT

                    if substract_background:
                        print("D... HERE I MUST DO subtraction of mask")
                        print("D... HERE I MUST DO subtraction of mask")
                        print("D... HERE I MUST DO subtraction of mask")
                        senh.subtract()

                    # - compensate for speed of the sky
                    if (speedx!=0) or (speedy!=0):
                        senh.translate( speedx, speedy)

                    if restart_translate:
                        senh.reset_camera_start()
                        restart_translate = False

                    # average  THIS IS HERE to be changed TOO (ACCUM)
                    # print("i.... average", average)

                    #print("i... GAMMAS ", gamma, gammadef )
                    if gamma_divide:
                        gamma_divide = False
                        if "gamma" in capa:
                            cc.set_gamma( int(gamma/2) )

                    if gamma_multiply:
                        gamma_multiply = False
                        if "gamma" in capa:
                            cc.set_gamma( int(gamma*2) )

                    if gamma_setdef:
                        gamma_setdef = False
                        if "gamma" in capa:
                            cc.setdef_gamma( )

                    if gain_divide:
                        gain_divide = False
                        if "gain" in capa:
                            cc.set_gain( int(gain/2) )

                    if gain_multiply:
                        gain_multiply = False
                        if "gain" in capa:
                            cc.set_gain( int(gain*2) )

                    if gain_setdef:
                        gain_setdef = False
                        if "gain" in capa:
                            cc.setdef_gain( )


                    #--------------- now apply labels ------i cannot get rid in DETM---
                    #--------- all this will be on all rames histo,detect,direct,delta
                    senh.setbox(" ", senh.TIME)
                    if target_frame in ["detect","delta","histo"]:
                        senh.setbox(f"DISP {target_frame}",senh.DISP)
                    if average>0:
                        senh.setbox(f"acc {average}",  senh.avg)
                    if blur>0:
                        senh.setbox(f"blr  {blur}",  senh.blr)
                    if threshold>0:
                        senh.setbox(f"trh  {threshold}",  senh.trh)
                    if timelaps>0:
                        senh.setbox(f"laps {timelaps}",  senh.lap)
                    if histogram:
                        senh.setbox(f"his {hmean:3.0f}",  senh.hist)
                    if speedx!=0:
                        #print(speedx)
                        senh.setbox(f"x {speedx:.3f}",  senh.speedx)
                    if speedy!=0:
                        senh.setbox(f"y {speedy:.3f}",  senh.speedy)


                    # ----------------expo gain gamma
                    # very stupid camera    ZC0303 Webcam
                    if "exposure" in capa:
                        if exposure!=exposuredef: # manual
                            senh.setbox(f"expo {exposure}",  senh.expo)

                    if "exposure_auto" in capa:
                        if expo_auto!=expo_autodef: # manual
                            senh.setbox(f"expo {exposure_absolute}",  senh.expo)

                    if ("gain" in capa) and (gain!=gaindef): # gain is not frequently tunable
                        senh.setbox(f"g {gain}",  senh.gain)

                    if ("gamma" in capa):
                        if (gamma!=gammadef): # manual
                            senh.setbox(f"m {gamma}",  senh.gamma)


                    # ----  for detmo ---- work with detect motion--------------------
                    if (threshold>0) :
                        senh.setbox("MODE DM", senh.MODE) #---push UP to avoid DetMot
                        senh.detmo( average, blur)
                        senh.chk_threshold( threshold )
                        if senh.motion_detected:
                            # print("D... sav mot", senh.motion_detected)
                            senh.save_avi( seconds = -1, name = "dm" )
                    else:
                        senh.setaccum( average  )
                        senh.setblur( blur )
                        #senh.setbox("MODE  ", senh.MODE)

                    # ---draw histogram
                    if target_frame == "histo":
                        senh.histo( )

                    if timelaps>0:
                        senh.save_avi( seconds = timelaps )



                    #------------yield the resulting frame-----------------------------
                    if target_frame in ["detect","delta","histo"]:
                        frame = senh.get_frame(  typ = target_frame)
                    else:
                        frame = senh.get_frame(  )

            yield frame



    @staticmethod
    def set_video_source(source):

        print("D... set_video_source: source=", source)
        camera = cv2.VideoCapture( source,  cv2.CAP_V4L2)
        print("D... ",camera)
        print("D... setting MJPG writer....FMP4 works too")
        # camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('F','M','P','4'))
        print("D... first camera read ....")
        ok = False
        try:
            _, img = camera.read()
            print(img.size) # this can fail and reset to DEV 0
            ok = True
        except Exception as ex:
            print("X... CAMERA read ... FAILED",ex)

        if ok:
            return camera
        return None
