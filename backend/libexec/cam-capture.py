#!/usr/bin/python3
##
## pyaicam/backend/libexec/cam-capture.py
##

import pyaicam.presentation #camera2_pb2

import grpc

import re
import sys
import time

import concurrent #futures
import threading

from pyaicam.application.logging import *
logger = getLogger('cam-capture')


class CameraControllerServicer(
    pyaicam.presentation.CameraControllerServicer
):

    def ControlStream(self, request, context):
        pass


def start_server() -> grpc.Server:
    port = "50051"
    server = grpc.server(
        concurrent.futures.ThreadPoolExecutor(max_workers=1)
    )
    pyaicam.presentation.add_CameraControllerServicer_to_server(
        CameraControllerServicer(), server
    )
    server.add_insecure_port("[::]:" + port)
    server.start()
    print(f'*** Server ready: dns:127.0.0.1:{port}')
    return server


def stop_server(server: grpc.Server, grace: int|None = 10):
    server.stop(grace)
    server.wait_for_termination()


def main():
    server = start_server()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        print('\n*** Stopping...')
        stop_server(server)


if __name__ == '__main__':
    main()

#--#
