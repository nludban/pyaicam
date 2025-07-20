##
## pyaicam.presentation.cameraproxy
##

from . import camera2_pb2
from . import camera2_pb2_grpc

from .camera2_pb2 import (
    ArraySize,
    SensorWindow,
    SensorConfig,
    ExposureLimits,
    ExposureControls,
    StreamConfig,

    # For type checking
    NextCommand,
    Configure,
    Subscribe,
    Unsubscribe,
    Capture,
    Reset,
    Close,
)

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

    def control_stream(self, agent: 'CameraAgent'):
        nc = agent.on_initialize(self)
        while True:
            if nc.has_configure():
                nc = agent.on_configure(nc.configure)
            elif nc.has_subscribe():
                nc = agent.on_configure(nc.subscribe)
            elif nc.has_unsubscribe():
                nc = agent.on_unsubscribe(nc.unsubscribe)
            elif nc.has_reset():
                nc = agent.on_reset(nc.reset)
            elif nc.has_close():
                nc = agent.on_close(nc.close)
            else:
                raise ValueError(nc)
        # except -> agent.on_error(...)

    def update_standby(self) -> NextCommand:
        pass

    def update_ready(self) -> NextCommand:
        pass

    def update_running(self) -> NextCommand:
        pass

    def update_fault(self) -> NextCommand:
        pass


class CameraAgent:

    def get_host(self) -> str:
        raise NotImplementedError(f'{self.__class__}.get_host')

    def get_camera_id(self) -> str:
        raise NotImplementedError(f'{self.__class__}.get_camera_id')

    def on_initialize(
        self, proxy: CameraProxy
    ) -> NextCommand:
        raise NotImplementedError(f'{self.__class__}.on_initialize')

    def on_configure(
        self, proxy: CameraProxy, req: Configure
    ) -> NextCommand:
        raise NotImplementedError(f'{self.__class__}.on_configure')

    def on_subscribe(
        self, proxy: CameraProxy, req: Subscribe
    ) -> NextCommand:
        raise NotImplementedError(f'{self.__class__}.on_subscribe')

    def on_unsubscribe(
        self, proxy: CameraProxy, req: Unsubscribe
    ) -> NextCommand:
        raise NotImplementedError(f'{self.__class__}.on_unsubscribe')

    def on_reset(
        self, proxy: CameraProxy, req: Reset
    ) -> NextCommand:
        raise NotImplementedError(f'{self.__class__}.on_reset')

    def on_close(
        self, proxy: CameraProxy, req: Close
    ) -> NextCommand:
        raise NotImplementedError(f'{self.__class__}.on_close')

    #def on_error(...) -> None
    

#--#
