FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt


RUN  docker-compose up -d 

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/app/app


CMD ["python3", "app/main.py"]