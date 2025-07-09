FROM python:3.11

WORKDIR /pyaicam-api

COPY /pyaicam ./pyaicam
COPY /bin ./bin
COPY /libexec ./libexec
COPY /requirements.txt .

RUN pip install -r requirements.txt

#CMD uvicorn main:app --host 0.0.0.0 --port 8000 --reload
