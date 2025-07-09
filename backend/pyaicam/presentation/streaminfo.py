##
## pyaicam.presentation.streaminfo
##

import pydantic

import picamera2.formats

from typing import Literal


class StreamInfo(pydantic.BaseModel):

    name: str
    format: Literal[tuple(picamera2.formats.ALL_FORMATS)]
    size: tuple[int, int]
    stride: int
    framesize: int

#--#
