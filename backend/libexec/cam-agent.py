#!/usr/bin/python3
##
## pyaicam/backend/libexec/cam-agent.py
##

import pyaicam.presentation.camera2_pb2

from pyaicam.application.logging import *

import re
import sys
import time

import threading

import libcamera
import picamera2

logger = getLogger('cam-agent')

#---------------------------------------------------------------------#

infos = picamera2.Picamera2.global_camera_info()
logger.info('Detected cameras', **log_extra(count=len(infos)))

for info in infos:
    logger.info('Detected camera info',
                **log_extra(num=info['Num'],
                            location=info['Location'],
                            model=info['Model'],
                            rotation=info['Rotation'],
                            id=info['Id']))

arg0, camera_id, target_url = sys.argv
if re.match(r'[0-9]+', camera_id):
    camera_id = infos[int(camera_id)]['Id']
camera_info = [ info for info in infos
                if info['Id'] == camera_id ][0]

# target_url:
# dns:<host>:<port>
# ipv4:<addr>:<port>

## Test connection to server, announce agent startup?

logger.info('Opening camera', **log_extra(id=camera_info['Id']))


#--#
