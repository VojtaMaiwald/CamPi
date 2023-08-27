#!/usr/bin/python3

"""
Available cameras
-----------------
0 : imx519 [4656x3496] (/base/soc/i2c0mux/i2c@1/imx519@1a)
    Modes: 'SRGGB10_CSI2P' : 1280x720 [80.01 fps - (1048, 1042)/2560x1440 crop]
                             1920x1080 [60.05 fps - (408, 674)/3840x2160 crop]
                             2328x1748 [30.00 fps - (0, 0)/4656x3496 crop]
                             3840x2160 [18.00 fps - (408, 672)/3840x2160 crop]
                             4656x3496 [9.00 fps - (0, 0)/4656x3496 crop]

"""

import cv2
from libcamera import controls
from picamera2 import Picamera2
import time

stop = False

picam2 = Picamera2()
#picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 408)}, raw={"size": (4656, 3496)}))
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}, raw={"size": (2328, 1748)}))
#picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 360)}, raw={"size": (1280, 720)}))

picam2.start()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous, "AfSpeed": controls.AfSpeedEnum.Fast})

while not stop:
    start = time.time()
    im = picam2.capture_array()
    end = time.time()

    print(f"{1//(end - start)}   ", end="\r")

    cv2.imshow("Camera", im)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        stop = True

picam2.stop_preview()
picam2.stop()