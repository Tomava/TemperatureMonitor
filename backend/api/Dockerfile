FROM python:3.12

RUN useradd -m -u 1000 scripter

RUN mkdir /app

#RUN apt update && apt install -y cmake

USER scripter
WORKDIR /app

COPY *.py ./
COPY requirements.txt ./
COPY .env ./

#ENV PATH="/usr/local/bin/cmake:${PATH}"

RUN pip3 install -r requirements.txt
