from flask import Flask
from flask import render_template
from flask import request
import yaml
from flask_mysqldb import MySQL

app = Flask(__name__)

# DB congig

db = yaml.load(open('db.yaml'))

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route("/", methods=['GET', 'POST'])
def landing():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO user(username, password) VALUES(%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('index.html')


@app.route("/auth", methods=['POST'])
def isAuth():
    userDetails = request.form
    username = userDetails['username']
    password = userDetails['password']
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT username,password FROM user", (username, password)
    )
    mysql.connection.commit()
    cur.close()
    return 'success'
