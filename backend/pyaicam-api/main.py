from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#from 
from mjpegreader import MjpegReader


app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/pyaicam-api/")
async def get_root_api():
    """[summary]
    Test EP Summary

    [description]
    Description of Test EP
    """
    return [{"name": "cook"}, {"name": "pipsi"}]

#--#
