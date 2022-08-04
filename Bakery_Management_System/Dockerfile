FROM python:3
ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /BakeryApp DRF
COPY requirements.txt requirements.txt
RUN pip3 install djangorestframework
RUN pip3 install -r requirements.txt
COPY . .