##
## pyaicam.presentation.cameraproxy
##

from . import camera2_pb2
from . import camera2_pb2_grpc

import grpc

import os

#---------------------------------------------------------------------#

class CameraProxy:

    def __init__(self, server_uri):
        self._channel = grpc.insecure_channel(server_uri)
        self._stub = camera2_pb2_grpc.CameraControllerStub(
            self._channel)

    def agent_starting(
        self, host: str, camera_id: str, reason: str
    ) -> None:
        pid = os.getpid()
        agent_info = camera2_pb2.AgentInfo(
            host=host, pid=pid, camera_id=camera_id, reason=reason
        )
        self._stub.AgentStarting(agent_info)

    def agent_stopping(
        self, host: str, camera_id: str, reason: str
    ) -> None:
        pid = os.getpid()
        agent_info = camera2_pb2.AgentInfo(
            host=host, pid=pid, camera_id=camera_id, reason=reason
        )
        self._stub.AgentStopping(agent_info)

#--#
