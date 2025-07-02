# pyaicam

Raspberry Pi as IP Camera platform for AI things

"pie-eye-cam"

A very new project - currently importing functionality from several
very old projects to the modern web stacks.


## ConOps

Attach any camera supported by [picamera2](https://github.com/raspberrypi/picamera2)
to any [Raspberry Pi](https://www.raspberrypi.com/), deploy the backend and
frontend using docker, get an IP Camera.

Configurable stream encoding, size / quality / framerate, exposure, etc...

Multiple cameras or streams are possible depending on the Pi model...

API provided for programmatic access and control, specifically to make
it easy to experiment with DSP and AI.
Expect a client library to keep it simple.


## Build

### Backend

The backend is a FastAPI app interfacing to a camera.

`(cd backend && docker compose up)`

http://192.168.1.172:8000/pyaicam-api/


### Frontend

The frontend is a React/Next.js app providing web UI for status, manual
camera control, and observation.

`(cd frontend && docker compose up)`

http://192.168.1.172:3000/ (todo: should be pyaicam-view here)

##
