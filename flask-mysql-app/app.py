from flask import Flask, jsonify
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
                                             address VARCHAR(250) NOT NULL, PRIMARY KEY (`id`));''')
    cursor.close()
    return 'Tabla Creada'


@app.route('/add-students')
def addstudents():
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO students (id,name,email,phone,address) VALUES(1,'Pedro Romero','pedro_romero@gmail.com',657798564,'Sant JOan DEspi');
                       INSERT INTO students (id,name,email,phone,address) VALUES(2,'Nazaret Olivieri', 'nazaret_olivieri@gmail.com',610432987,'Cornella de Llobregat'); ''')
    cursor.close()
    return 'Estudiantes añadidos'


@app.route('/')
def students():
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM students; ''')
    for row in cursor.fetchall():
        print('id:', row[0])
        print('name:', row[1])
        print('email:', row[2])
        print('phone:', row[3])
        print('address:', row[4])
        print("\n")

    cursor.close()
    return ('Todos los estudiantes mostrados')

@app.route('/ping')
def ping():
    return 'pong'
