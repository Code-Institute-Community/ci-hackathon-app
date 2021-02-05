FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install python3 python3-pip libmysqlclient-dev mysql-client vim -y

WORKDIR /hackathon-app
COPY ./requirements.txt /hackathon-app/requirements.txt

RUN pip3 install -r requirements.txt

COPY ./src/ /hackathon-app

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
