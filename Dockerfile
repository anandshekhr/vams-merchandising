# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install --index-url https://phonepe.mycloudrepo.io/public/repositories/phonepe-pg-sdk-python --extra-index-url https://pypi.org/simple phonepe_sdk
COPY . /code/