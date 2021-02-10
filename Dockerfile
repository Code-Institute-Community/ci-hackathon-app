FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install python3 python3-pip libmysqlclient-dev mysql-client vim -y

WORKDIR /hackathon-app
COPY ./requirements.txt /hackathon-app/requirements.txt

RUN pip3 install -r requirements.txt

COPY ./src/ /hackathon-app

EXPOSE 8000
ENTRYPOINT ["gunicorn", "--workers=5", "--timeout=120", "--access-logfile=-",\
            "--bind=0.0.0.0:8000", "--max-requests=1000", "main.wsgi:application"]
