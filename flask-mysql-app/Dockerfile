FROM python:3.7-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers curl mysql-client mysql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . ./

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
ENV MYSQL_USER=usuariodb
ENV MYSQL_PASSWORD=secret12345
ENV MYSQL_HOST=db
ENV MYSQL_DB=studentdb

EXPOSE 5000

CMD flask run
