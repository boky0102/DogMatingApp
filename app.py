from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from werkzeug.utils import redirect
import yaml
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import flask_login
from flask_login import UserMixin


app = Flask(__name__)

# DB congig

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

# APP SECRET KEY CONFIG

secret = yaml.load(open('appcfg.yaml'))
app.secret_key = secret['SECRET_KEY']
app.config['SESSION_TYPE'] = 'filesystem'

# BCRYPT CONFIG

bcrypt = Bcrypt(app)

# FLASK-LOGIN CONFIGURATION

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass

# FLASK-LOGIN USER LOADER FUNCTIONALITY


@login_manager.user_loader
def user_loader(username):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT username,password FROM user WHERE username = (%s)", (
            username,)
    )
    result = cur.fetchone()
    cur.close()

    if len(result) == 0:
        return
    else:
        user = User()
        user.id = result[0]
        return User

# UNAUTHORIZED REDIREC HANDLER


@login_manager.unauthorized_handler
def unathorized_handler():
    return redirect("/")

# LANDING PAGE ROUTE


@app.route("/", methods=['GET', 'POST'])
def landing():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT username FROM user WHERE username = (%s)", (username,))
        result = cur.fetchall()
        cur.close()
        if len(result) == 0:
            pw_hash = bcrypt.generate_password_hash(
                password, 10).decode('utf-8')
            cur2 = mysql.connection.cursor()
            cur2.execute(
                "INSERT INTO user(username, password) VALUES(%s, %s)", (username, pw_hash))
            mysql.connection.commit()
            cur2.close()
            return 'success'
        else:
            flash('Username already exists.')
            return redirect("/")

    return render_template('index.html')


@app.route("/auth", methods=['POST'])
def isAuth():
    userDetails = request.form
    username = userDetails['usernameLogin']
    password = userDetails['passwordLogin']

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT username,password FROM user WHERE username=(%s)", (
            username,)
    )
    result = cur.fetchall()
    cur.close()
    if len(result) > 0:
        pwToCheck = result[0][1]
        if bcrypt.check_password_hash(pwToCheck, password):
            print(result)
            user = User()
            user.id = username
            flask_login.login_user(user)
            return redirect("/home")
        else:
            flash('Wrong username or password')
            return redirect("/")
    else:
        flash('Wrong username or password')
        return redirect('/')


@app.route("/home", methods=['GET'])
@flask_login.login_required
def homeRoute():
    return render_template("home.html")


@app.route("/add-puppy", methods=['GET', 'POST'])
def userCheck():
    return 'add-puppy'


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect("/")
