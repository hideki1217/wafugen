FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y \
    python3 python3-pip \
    vim curl iputils-ping net-tools \
    make 

WORKDIR /workspace

COPY ./run.sh /workspace/run.sh
RUN chmod 777 /workspace/run.sh
COPY ./requirements.txt /workspace/requirements.txt

RUN pip install -r /workspace/requirements.txt