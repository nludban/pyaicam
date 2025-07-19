#!/usr/bin/python3
##
## pyaicam/backend/libexec/cam-capture.py
##

import pyaicam.presentation #camera2_pb2
import pyaicam.application.network

import grpc

import re
import sys
import time

import concurrent #futures
import threading

from google.protobuf.empty_pb2 import Empty

from pyaicam.application.logging import *
logger = getLogger('cam-capture')


class CameraControllerServicer(
    pyaicam.presentation.CameraControllerServicer
):

    def AgentStarting(self, request, context):
        print('Starting:', request)
        return Empty()

    def ControlStream(self, request, context):
        pass

    def AgentStopping(self, request, context):
        print('Stopping:', request)
        return Empty()


def start_server() -> grpc.Server:
    host = pyaicam.application.network.local_ipaddr()
    port = "50051"
    server = grpc.server(
        concurrent.futures.ThreadPoolExecutor(max_workers=1)
    )
    pyaicam.presentation.add_CameraControllerServicer_to_server(
        CameraControllerServicer(), server
    )
    # tcp46   0   0  *.50051   *.*     LISTEN
    #server.add_insecure_port("[::]:" + port)
    server.add_insecure_port(f'{host}:{port}')
    server.start()
    print(f'*** Server ready: dns:{host}:{port}')
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
