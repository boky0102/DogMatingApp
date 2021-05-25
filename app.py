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
from datetime import datetime
from flask import session


import os


app = Flask(__name__)

# DB congig

db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

# APP SECRET KEY CONFIG

secret = yaml.load(open('appcfg.yaml'), Loader=yaml.FullLoader)
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
        "SELECT UID,username,password FROM user WHERE username = (%s)", (
            username,)
    )
    result = cur.fetchone()
    cur.close()

    if result is None:
        return
    else:
        user = User()
        user.id = result[1]
        user.uid = result[0]
        return User

# UNAUTHORIZED REDIREC HANDLER


@login_manager.unauthorized_handler
def unathorized_handler():
    return redirect("/")


# UPLOAD ABSOLUTE PATH CONFIGURATION
UPLOAD_FOLDER = "./static/images/uploads"
app.config['IMAGE_UPLOADS'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'PNG', 'JPG', 'JPEG', 'GIF'}


def allowed_image(filename):
    if not "." in filename:
        return False
    else:
        ext = filename.rsplit(".", 1)[1]
        if ext.upper() in app.config['ALLOWED_EXTENSIONS']:
            return True
        else:
            return False

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
        "SELECT username,password,UID FROM user WHERE username=(%s)", (
            username,)
    )
    result = cur.fetchall()
    cur.close()
    if len(result) > 0:
        pwToCheck = result[0][1]
        if bcrypt.check_password_hash(pwToCheck, password):
            print(result)
            user = User()
            user.id = result[0][0]
            session["uid"] = result[0][2]
            session['username'] = result[0][0]
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
@flask_login.login_required
def addPuppy():
    if request.method == 'GET':
        return render_template('addpuppy.html')
    if request.method == 'POST':
        puppyDetails = request.form
        puppyname = puppyDetails['name']
        description = puppyDetails['description']
        breed = puppyDetails['breed']
        dateOfBirth = puppyDetails['birthDate']
        img = request.files['img']
        imgSrc = "./static/images/noavatar-dog.png"

        if request.files:

            if allowed_image(img.filename):
                time = datetime.now()
                dt_string = time.strftime("%d-%m-%Y%H-%M-%S")
                img.save(os.path.join(
                    app.config['IMAGE_UPLOADS'], img.filename))

                filename = str(img.filename)
                extension = filename.split(".")
                name = dateOfBirth + dt_string
                extension = str(extension[1])

                source = UPLOAD_FOLDER + "/" + filename
                renamed = UPLOAD_FOLDER + "/" + name + "." + extension
                os.rename(source, renamed)
                imgSrc = renamed

            else:
                return redirect("/add-puppy")
        uid = session["uid"]
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO dog(name,birth_day,species,description,avatar_src,UID) VALUES(%s,%s,%s,%s,%s,%s)", (
                puppyname, dateOfBirth, breed, description, imgSrc, uid)
        )
        mysql.connection.commit()
        cur.close()
        return redirect("/home")


@app.route('/profile', methods=['GET', 'POST'])
@flask_login.login_required
def profile():
    if request.method == 'GET':
        username = session['username']
        return render_template("profile.html", currentUsername=username)
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        streetAndNum = userDetails['streetAndNum']
        city = userDetails['city']
        country = userDetails['country']
        img = request.files['img']

        if request.files:

            if allowed_image(img.filename):
                time = datetime.now()
                dt_string = time.strftime("%d-%m-%Y%H-%M-%S")
                img.save(os.path.join(
                    app.config['IMAGE_UPLOADS'], img.filename))
                filename = str(img.filename)
                extension = filename.split(".")
                name = username + dt_string
                extension = str(extension[1])
                source = UPLOAD_FOLDER + "/" + filename
                renamed = UPLOAD_FOLDER + "/" + name + "." + extension
                os.rename(source, renamed)
                imgSrc = renamed
            else:
                return redirect("/add-puppy")

        uid = session['uid']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO address(street_and_num, city, country) VALUES(%s,%s,%s)", (
                streetAndNum, city, country)
        )

        cur.close()


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect("/")
