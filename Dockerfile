FROM python:3.12.10-bookworm

LABEL maintainer="Zhengmao Ye <yezhengmaolove@gmail.com>"
LABEL version="0.0.1"
LABEL description="textpy"

COPY . /app

RUN cd /app && pip install -e .