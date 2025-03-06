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
color = (255, 255, 255)
font = cv2.FONT_HERSHEY_DUPLEX
scale = 1.5
thickness = 2


picam2a = Picamera2(0)
preview_controls = {'FrameDurationLimits': (11111, 11111), 'Saturation': 0, 'AfMode': controls.AfModeEnum.Continuous}
picam2a_config = picam2a.create_preview_configuration(buffer_count=2, controls=preview_controls)
picam2a_config['main']['size'] = IMG_DIMS
picam2a_config['main']['format'] = 'YUV420';
picam2a.align_configuration(picam2a_config)
picam2a.configure(picam2a_config)


picam2b = Picamera2(1)
picam2b_config = picam2b.create_preview_configuration(buffer_count=2, controls=preview_controls)
picam2b_config['main']['size'] = IMG_DIMS
picam2b_config['main']['format'] = 'YUV420';
picam2b.align_configuration(picam2b_config)
picam2b.configure(picam2b_config)

def apply_huda(request):
	timestamp = time.strftime('%X')
	with MappedArray(request, 'main') as m:
		cv2.putText(m.array, timestamp, (240, 320), font, scale, color, thickness)
		
def apply_hudb(request):
	timestamp = time.strftime('%X')
	with MappedArray(request, 'main') as m:
		cv2.putText(m.array, timestamp, (240, 320), font, scale, color, thickness)

picam2a.start_preview(Preview.QTGL, x=0, y=-100, width=1080, height=1200)
picam2b.start_preview(Preview.QTGL, x=2160, y=-100, width=1080, height=1200)
		
#picam2a.pre_callback = apply_huda
#picam2b.pre_callback = apply_hudb

picam2a.start()

picam2b.start()
	

input("Press Enter to close Preview...")
