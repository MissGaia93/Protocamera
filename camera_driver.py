#!/usr/bin/python3

import time
import board
import busio
import adafruit_bno055
import numpy as np
import cv2

from libcamera import controls
from picamera2 import Picamera2, Preview, MappedArray


IMG_DIMS = (1080, 700)
#i2c = busio.I2C(board.SCL, board.SDA)
#sensor = adafruit_bno055.BNO055_I2C(i2c)
color = (0, 0, 0)
font = cv2.FONT_HERSHEY_DUPLEX
scale = 2
thickness = 1


picam2a = Picamera2(0)
preview_controls = {'FrameDurationLimits': (11111, 11111), 'Saturation': 0, 'AfMode': controls.AfModeEnum.Continuous}
picam2a_config = picam2a.create_preview_configuration(buffer_count=1, controls=preview_controls)
picam2a_config['main']['size'] = IMG_DIMS
picam2a_config['main']['format'] = 'YUV420';
picam2a.align_configuration(picam2a_config)
picam2a.configure(picam2a_config)

picam2b = Picamera2(1)
picam2b_config = picam2b.create_preview_configuration(buffer_count=1, controls=preview_controls)
picam2b_config['main']['size'] = IMG_DIMS
picam2b_config['main']['format'] = 'YUV420';
picam2b.align_configuration(picam2b_config)
picam2b.configure(picam2b_config)

picam2a.start_preview(Preview.QTGL, x=0, y=-100, width=1080, height=1200)
picam2b.start_preview(Preview.QTGL, x=2160, y=-100, width=1080, height=1200)

def apply_timestamp(request):
	timestamp = time.strftime('%Y-%n-%d %X')
	with MappedArray(request, 'main') as m:
		cv2.putText(m.array, timestamp, (500, 600), font, scale, color, thickness)
		
picam2a.pre_callback = apply_timestamp

picam2a.start()
#with picam2a.controls as ctrl:
	#ctrl.FrameDurationLimits = 11111
	#ctrl.Framerate = 90

picam2b.start()
#with picam2b.controls as cntrl:
	#ctrl.FrameDurationLimits = 11111
	#ctrl.Framerate = 90

#def HUD
	

input("Press Enter to close Preview...")
