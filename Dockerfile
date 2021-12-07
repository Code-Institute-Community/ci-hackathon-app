FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install python3 python3-pip libmysqlclient-dev mysql-client vim -y

WORKDIR /hackathon-app
COPY ./requirements.txt /hackathon-app/requirements.txt

RUN pip3 install -r requirements.txt

COPY ./accounts/ /hackathon-app/accounts/
COPY ./assets/ /hackathon-app/assets/
COPY ./custom_slack_provider/ /hackathon-app/custom_slack_provider/
COPY ./hackathon/ /hackathon-app/hackathon/
COPY ./home/ /hackathon-app/home/
COPY ./images/ /hackathon-app/images/
COPY ./main/ /hackathon-app/main/
COPY ./profiles/ /hackathon-app/profiles/
COPY ./resources/ /hackathon-app/resources/
COPY ./showcase/ /hackathon-app/showcase/
COPY ./static/ /hackathon-app/static/
COPY ./teams/ /hackathon-app/teams/
COPY ./templates/ /hackathon-app/templates/
COPY ./hackadmin/ /hackathon-app/hackadmin/
COPY ./manage.py /hackathon-app/manage.py

EXPOSE 8000
ENTRYPOINT ["gunicorn", "--workers=5", "--timeout=120", "--access-logfile=-",\
            "--bind=0.0.0.0:8000", "--max-requests=1000", "main.wsgi:application"]
