from __future__ import absolute_import, print_function, division
from pymba import *
import numpy as np
import cv2
import time
import signal
import sys
import datetime as dt
from nep import*

sub = subscriber("/trigger", True)
pub = publisher("/camera1", False)

def signal_handler(signal, frame):
    """Signal handler used to close the app"""
    print('Signal Handler, you pressed Ctrl+C!')
    print('Exit in 2 seconds...')
    time.sleep(2)
    # clean up after capture
    camera0.revokeAllFrames()
    # close camera
    camera0.closeCamera()
    sys.exit()
    
# New signal handler    
signal.signal(signal.SIGINT, signal_handler)


# start Vimba
with Vimba() as vimba:
    # get system object
    system = vimba.getSystem()

    # list available cameras (after enabling discovery for GigE cameras)
    if system.GeVTLIsPresent:
        system.runFeatureCommand("GeVDiscoveryAllOnce")
        time.sleep(0.2)
    cameraIds = vimba.getCameraIds()
    for cameraId in cameraIds:
        print('Camera ID:', cameraId)

    # get and open a camera
    camera0 = vimba.getCamera(cameraIds[0])
    camera0.openCamera()

    # list camera features
    cameraFeatureNames = camera0.getFeatureNames()
    for name in cameraFeatureNames:
        print('Camera feature:', name)

    # read info of a camera feature
    #featureInfo = camera0.getFeatureInfo('AcquisitionMode')
    #for field in featInfo.getFieldNames():
    #    print field, '--', getattr(featInfo, field)

    # get the value of a feature
    print(camera0.AcquisitionMode)

    # set the value of a feature
    camera0.AcquisitionMode = 'SingleFrame'

    # create new frames for the camera
    frame0 = camera0.getFrame()    # creates a frame
    frame1 = camera0.getFrame()    # creates a second frame

    # announce frame
    frame0.announceFrame()

    # capture a camera image
    count = 0
    while True:
        success, info = sub.listen_info(False)
        if success:
            n1= dt.datetime.now()
            camera0.startCapture()
            frame0.queueFrameCapture()
            camera0.runFeatureCommand('AcquisitionStart')
            camera0.runFeatureCommand('AcquisitionStop')
            frame0.waitFrameCapture()
            msg = {'trigger':str(n1)}
            pub.send_info(msg)
            
            # get image data...
            imgData = frame0.getBufferByteData()
            print (n1)
            
            moreUsefulImgData = np.ndarray(buffer = frame0.getBufferByteData(),
                                           dtype = np.uint8,
                                           shape = (frame0.height,
                                                    frame0.width,
                                                    1))
            rgb = cv2.cvtColor(moreUsefulImgData, cv2.COLOR_BAYER_RG2RGB)
            #cv2.imwrite('foo.png'.format(count), rgb)
            #print("image saved".format(count))
            count += 1
            #cv2.imshow('frame',rgb)
            camera0.endCapture()
            #cv2.waitKey(10)
    # clean up after capture
    camera0.revokeAllFrames()
    # close camera
    camera0.closeCamera()

