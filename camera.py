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
from fps import FPS

MODE = 2

def main():
    stop = False
    fps = FPS(100)
    picam2 = Picamera2()
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    mode = picam2.sensor_modes[MODE]
    #main = {"format": 'XRGB8888', "size": (640, 480 if MODE in [2, 4] else 360)}
    #main = {"format": 'XRGB8888', "size": mode["size"]}
    main = {"format": 'XRGB8888', "size": (mode["size"][0]//2, mode["size"][1]//2)}
    picam2.configure(picam2.create_preview_configuration(main = main, raw = mode))

    picam2.start()
    picam2.set_controls({
        "AfMode": controls.AfModeEnum.Continuous,
        "AfSpeed": controls.AfSpeedEnum.Fast,
        "FrameRate": mode["fps"]
        })

    while not stop:
        start = time.time()
        image = picam2.capture_array()
        end = time.time()
        fps.addFrameTime(end - start)

        cv2.putText(image, f"FPS: {fps.getFps()}", (0, 20), font, 0.75, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(image, f"Res: {image.shape[1]}x{image.shape[0]}", (150, 20), font, 0.75, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow("Camera", image)
    
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            stop = True

    picam2.stop_preview()
    picam2.stop()

if __name__ == '__main__':
    main()