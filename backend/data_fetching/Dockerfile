FROM python:3.12

RUN useradd -m -u 1000 scripter
RUN groupadd -g 998 i2c
RUN usermod -aG i2c scripter

RUN mkdir /app

USER scripter
WORKDIR /app

COPY *.py ./
COPY requirements.txt ./
COPY .env ./

RUN pip3 install -r requirements.txt
