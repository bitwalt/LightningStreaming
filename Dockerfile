FROM python:3.10-slim-bullseye

LABEL maintainter "Walter M"

WORKDIR /workspace/

RUN apt-get update && apt-get upgrade -y


COPY . .
RUN pip install --upgrade pip
RUN pip install opencv-python 
RUN pip install loguru p2pnetwork


