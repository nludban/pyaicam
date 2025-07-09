##
## pyaicam.presentation.cameraconfig
##

from .sensorcaps import SensorMode

import pydantic

from typing import Any


class CameraConfig:

    transform
    color_space
    buffer_count: int
    queue: bool
    sensor: SensorMode
    raw: CameraInfo|None
    main: CameraInfo|None
    lores: CameraInfo|None
    controls: dict[str, Any]
    #display (preview?)

#--#
