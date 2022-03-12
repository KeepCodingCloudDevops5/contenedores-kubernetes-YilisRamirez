from flask import Flask
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']
app.config['MYSQL_DB'] = os.environ['MYSQL_DB']
mysql = MySQL(app)


@app.route('/create-table')
def createtable():
    cursor = mysql.connection.cursor()
    cursor.execute(''' CREATE TABLE students(id INT NOT NULL AUTO_INCREMENT,
                                             name VARCHAR(50) NOT NULL,
                                             email VARCHAR(100) NOT NULL,
                                             phone INT NOT NULL,
                                             address VARCHAR(250) NOT NULL, PRIMARY KEY (`id`)) ''')
    cursor.close()
    return 'Tabla Creada'


@app.route('/add-students')
def addstudents():
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO students (id,name,email,phone,address) VALUES(1,'Pedro Romero','pedro_romero@gmail.com',657798564,'Sant Joan DEspi');
                       INSERT INTO students (id,name,email,phone,address) VALUES(2,'Nazaret Olivieri','nazaret_olivieri@gmail.com',610432987,'Cornella de Llobregat'); commit; ''')
    cursor.close()
    return 'Estudiantes añadidos del primer año'


@app.route('/')
def students():
    s = "<table style='border:1px solid red'>"

    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM students; ''')
    for row in cursor.fetchall():
        s = s + "<tr>"
        for x in row:
            s = s + "<td>" + str(x) + "</td>"
        s = s + "</tr>"

    cursor.close()
    return "<html><body>" + s + "</body></html>"

@app.route('/ping')
def ping():
    return 'pong'
