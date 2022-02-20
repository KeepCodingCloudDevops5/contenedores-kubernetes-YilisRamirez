FROM python:3.7-alpine
RUN apk add gcc musl-dev linux-headers
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN pip install PyMySql
RUN pip install mysqlclient
EXPOSE 5000
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
CMD flask run
