from flask import Flask, jsonify
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

app = Flask(__name__)

def get_db():
    client = MySQL(host='mysql_db',
                         port='3306',
                         username='root',
                         password='passw',
                         authSource='admin')
    db = client["student_db"]
    return db

@app.route('/')
def ping_server():
    return "Welcome back to class."

@app.route('/students')
def get_stored_students():
    db=""
    try:
        db = get_db()
        _students = db.student_tb.find()
        students = [{"DNI": student["DNI"], "name": student["name"], "course": student["course"]} for student in _students]
        return jsonify({"students": students})
    except:
        pass
    finally:
        if type(db)==MySQL:
            db.close()

if __name__=='__main__':
     app.run(host="0.0.0.0", port=5000)

