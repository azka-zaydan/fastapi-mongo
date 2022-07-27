FROM ubuntu:latest

RUN apt update && apt upgrade -y

RUN apt install -y -q docker python3-dev build-essential python3-pip docker-compose docker

COPY ./requirements.txt /code/requirements.txt

COPY ./docker-compose.yml /code/docker-compose.yml

RUN pip3 install -r /code/requirements.txt

RUN docker-compose up -d

COPY ./src /code

CMD ["python3", "/code/main.py"]