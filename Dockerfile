FROM python:3.8-slim

RUN apt-get update && apt-get install -y curl

RUN apt-get install -y g++ unixodbc-dev git

COPY . /opt/app

WORKDIR /opt/app

RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "/opt/app/entrypoint.sh"]

EXPOSE 8000
