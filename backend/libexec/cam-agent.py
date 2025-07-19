#!/usr/bin/python3
##
## pyaicam/backend/libexec/cam-agent.py
##

import pyaicam.presentation

from pyaicam.application.logging import *
import pyaicam.application.network

import os
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

arg0, camera_id, server_url = sys.argv
if re.match(r'[0-9]+', camera_id):
    camera_id = infos[int(camera_id)]['Id']
camera_info = [ info for info in infos
                if info['Id'] == camera_id ][0]

# server_url:
# dns:<host>:<port>
# ipv4:<addr>:<port>

def run():
    host = pyaicam.application.network.local_ipaddr()

    proxy = pyaicam.presentation.CameraProxy(server_url)
    proxy.agent_starting(host, camera_id, 'Hello!')

    proxy.agent_stopping(host, camera_id, 'Good-bye.')



## Test connection to server, announce agent startup?

logger.info('Opening camera', **log_extra(id=camera_info['Id']))

run()


#--#
