FROM python:3.7-alpine
RUN apk add gcc musl-dev linux-headers curl mysql-client mysql-dev
WORKDIR /app
COPY . ./
RUN pip install -r requirements.txt
EXPOSE 5000
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV MYSQL_USER=usuariodb
ENV MYSQL_PASSWORD=secret12345
ENV MYSQL_HOST=db
ENV MYSQL_DB=studentdb
CMD flask run
