FROM python:3.14
WORKDIR /usr/src/app
COPY . .
RUN pip install -e .