##
## pyaicam.presentation.sensorscaps
##

import pydantic

import picamera2.formats

from typing import Literal


# _CSI2P => packed; otherwise extended to 8 or 16
# Pi5 => non-_CSI2P is ~lossless compressed raw format
# Pi5 => uncompressed = left shift to 16bpp

# request via sensor={output_size=<size>, bit_depth=<bit_depth>}
# request compat via raw stream

# request != .camera_configuration()

class SensorMode(pydantic.BaseModel):

    format: Literal[tuple(picamera2.formats.BAYER_FORMATS)]
    unpacked: Literal[tuple(picamera2.formats.BAYER_FORMATS)]
    bit_depth: int
    size: tuple[int, int]
    fps: float
    crop_limits: tuple[int, int, int, int]
    exposure_limits: tuple[int, int, int]


class SensorCaps(pydantic.BaseModel):

    modes: list[SensorMode]

#--#
