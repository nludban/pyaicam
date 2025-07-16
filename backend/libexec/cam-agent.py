#!/usr/bin/python3
##
## pyaicam/backend/libexec/cam-agent.py
##

import pyaicam.presentation.camera2_pb2

import logging
import sys
import time

import threading

import libcamera
import picamera2

#---------------------------------------------------------------------#

def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
               func=None, extra=None, sinfo=None):
    # logging.Logger
    rv = logging_makeRecord(self,
                            name, level, fn, lno, msg, args, exc_info,
                            func=func, extra=None, sinfo=sinfo)
    rv.extra = extra
    #print('Added extra', id(rv), extra)
    return rv

# `import logging` sets up root and manager as side effects.
# Workaround is to monkey patch the method on the class.
logging_makeRecord = logging.Logger.makeRecord
logging.Logger.makeRecord = makeRecord

class ExtraFormatter(logging.Formatter):
    converter = time.gmtime

    def formatMessage(self, record):
        base = super().formatMessage(record)
        if not record.extra:
            return base
        extra = [ '%s=%r' % key_value
                  for key_value in record.extra.items() ]
        return base + ' ' + ' '.join(extra)
    
# basicConfig accepts formatter=... starting in 3.15
logging.Formatter = ExtraFormatter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
    # XXX microseconds?
    #datefmt='%Y-%m-%d %H:%M_%S')
    #formatter=log_formatter)	# XXX py3.15
)

logger = logging.getLogger('cam-agent')

def log_extra(**kwargs):
    return {'extra': kwargs}

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


#--#
