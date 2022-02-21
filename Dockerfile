FROM python:3.9-buster as build

LABEL maintainter "Walter M"

WORKDIR /workspace/

RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3 python3-pip -y

COPY . /workspace/

# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
RUN pip install opencv-pyth¶on
RUN pip install pyshine
RUN pip install numpy
RUN pip install imutils
RUN pip install protobuf 
RUN pip install grpcio 
RUN pip install grpcio-tools 

RUN chmod +x /workspace/build_grpc.sh   
RUN /workspace/build_grpc.sh
