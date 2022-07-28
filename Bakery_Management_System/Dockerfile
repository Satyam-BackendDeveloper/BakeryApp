FROM python:3
ENV PYTHONBUFFERED 1
WORKDIR /BakeryApp
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .