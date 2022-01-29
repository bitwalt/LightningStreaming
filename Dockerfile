FROM python:3.10-slim-bullseye

LABEL maintainter "Walter M"

WORKDIR /workspace/

RUN apt-get update && apt-get upgrade -y


COPY . /workspace/

# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
RUN pip install opencv-pyth¶on
# RUN pip install opencv-contrib-python
RUN pip install pyshine
RUN pip install numpy
RUN pip install imutils
