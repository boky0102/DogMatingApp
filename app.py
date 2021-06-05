import os
from flask import Flask
from flask import render_template
from flask import request
from flask import flash
import flask
from werkzeug.utils import redirect
import yaml
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import flask_login
from flask_login import UserMixin
from datetime import datetime
from flask import session
from breeds import breeds
from random import randint


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
            defaultAvatar = "/static/images/noavatar-dog.png"
            pw_hash = bcrypt.generate_password_hash(
                password, 10).decode('utf-8')
            cur2 = mysql.connection.cursor()
            cur2.execute(
                "INSERT INTO user(username, password, img_src) VALUES(%s, %s, %s)", (username, pw_hash, defaultAvatar))
            mysql.connection.commit()
            cur2.close()
            return redirect("/")
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
        "SELECT username,password,UID,img_src FROM user WHERE username=(%s)", (
            username,)
    )
    result = cur.fetchall()
    cur.close()
    if len(result) > 0:
        pwToCheck = result[0][1]
        if bcrypt.check_password_hash(pwToCheck, password):
            user = User()
            user.id = result[0][0]
            session["uid"] = result[0][2]
            session['username'] = result[0][0]
            session['avatSrc'] = result[0][3]
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
    return render_template("home.html", currentAvatar=session['avatSrc'])


@app.route("/add-puppy", methods=['GET', 'POST'])
@flask_login.login_required
def addPuppy():
    if request.method == 'GET':
        return render_template('addpuppy.html', currentAvatar=session['avatSrc'], breedOptions=breeds)
    if request.method == 'POST':
        puppyDetails = request.form
        puppyname = puppyDetails['name']
        description = puppyDetails['description']
        breed = puppyDetails['breed']
        gender = puppyDetails['gender']
        dateOfBirth = puppyDetails['birthDate']
        img = request.files['img']
        imgSrc = "./static/images/noavatar-dog.png"
        playful = int(puppyDetails['playful'])
        curious = int(puppyDetails['curious'])
        social = int(puppyDetails['social'])
        aggressive = int(puppyDetails['aggressive'])
        demanding = int(puppyDetails['demanding'])
        dominant = int(puppyDetails['dominant'])
        protective = int(puppyDetails['protective'])
        apartment = int(puppyDetails['apartment'])
        vocal = int(puppyDetails['vocal'])

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

        time = datetime.now()
        dt_string = time.strftime("%d-%m-%Y%H-%M-%S")
        tid = dt_string + str(randint(0, 10000))
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO traits(TID,playful,curious,social,aggressive,demanding,dominant,protective,apartment,vocal) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                tid, playful, curious, social, aggressive, demanding, dominant, protective, apartment, vocal)
        )
        mysql.connection.commit()
        cur.close()

        uid = session["uid"]
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO dog(name,birth_day,species,description,avatar_src,UID,TID,gender) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (
                puppyname, dateOfBirth, breed, description, imgSrc[1:], uid, tid, gender)
        )
        mysql.connection.commit()
        cur.close()
        return redirect("/home")


@app.route('/profile', methods=['GET', 'POST'])
@flask_login.login_required
def profile():
    if request.method == 'GET':
        username = session['username']

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT user.img_src, address.street_and_num, address.city, address.country FROM user INNER JOIN address ON user.AID = address.AID WHERE user.username = %s", (
                username,)
        )

        result = cur.fetchone()
        cur.close()

        if result is None:
            return render_template("profile.html", currentUsername=username, currentAvatar="", streetAndNum="", city="", country="")
        else:
            return render_template("profile.html", currentUsername=username, currentAvatar=result[0], streetAndNum=result[1], city=result[2], country=result[3])

    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        streetAndNum = userDetails['streetAndNum']
        city = userDetails['city']
        country = userDetails['country']
        img = request.files['img']

        imgSrc = "/static/images/default-avatar.png"
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
        mysql.connection.commit()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT AID FROM address WHERE street_and_num=(%s)", (
                streetAndNum,)
        )
        result = cur.fetchone()
        cur.close()

        if result is not None:
            aid = result[0]
            cur = mysql.connection.cursor()
            cur.execute(
                "UPDATE user SET username=(%s), img_src=(%s), AID=(%s) WHERE UID=(%s)", (
                    username, imgSrc[1:], aid, uid
                )
            )
            mysql.connection.commit()
            cur.close()
        session['avatSrc'] = imgSrc
        flash("Profile info changed successfully")
        return redirect("/profile")


@app.route('/explore', methods=['GET', 'POST'])
@flask_login.login_required
def explore():
    currentUserId = session['uid']
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM dog WHERE UID != %s", (currentUserId,)
        )
        result = cur.fetchall()
        cur.close()
        return render_template('explore.html', currentAvatar=session['avatSrc'], breedOptions=breeds, dogs=result)
    if request.method == 'POST':
        filterOptions = request.form
        breed = filterOptions['breed']
        gender = filterOptions['gender']
        cur = mysql.connection.cursor()

        if breed == "Any" and gender == "Any":
            cur.execute(
                "SELECT * FROM dog WHERE UID != %s", (currentUserId,)
            )
            result = cur.fetchall()
            return render_template('explore.html', currentAvatar=session['avatSrc'], breedOptions=breeds, dogs=result)

        elif breed == "Any" and gender != "Any":
            cur.execute(
                "SELECT * FROM dog WHERE UID != %s AND gender = %s", (
                    currentUserId, gender)
            )
        elif breed != "Any" and gender == "Any":
            cur.execute(
                "SELECT * FROM dog WHERE UID != %s AND species = %s", (
                    currentUserId, breed
                )
            )
        else:
            cur.execute(
                "SELECT * FROM dog WHERE UID != %s AND species = %s AND gender = %s", (
                    currentUserId, breed, gender
                )
            )
        results = cur.fetchall()
        return render_template('explore.html', currentAvatar=session['avatSrc'], breedOptions=breeds, dogs=results)


@app.route('/dog/<dogid>', methods=['GET', 'POST'])
@flask_login.login_required
def getDog(dogid):
    thisId = dogid
    if request.method == 'GET':
        print(session['avatSrc'])
        curAvatSrc = session['avatSrc']
        curAvatSrc = curAvatSrc

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT d.name, d.description, d.birth_day, d.species, d.avatar_src, u.username, u.img_src, d.gender, t.playful, t.curious, t.social, t.aggressive, t.demanding, t.dominant, t.protective, t.apartment, t.vocal, d.uid FROM dog d INNER JOIN user u ON d.UID = u.UID INNER JOIN traits t ON  d.TID = t.TID WHERE d.DID = %s", (
                dogid,)
        )
        result = cur.fetchone()
        cur.close()
        print(result)

        dogPicture = result[4]
        ownerPicture = result[6]
        traitNames = ['PLAYFULL', 'CURIOUS', 'SOCIAL', 'AGGRESSIVE',
                      'DEMANDING', 'DOMINANT', 'PROTECTIVE', 'APARTMENT', 'VOCAL']

        uid = session['uid']
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT name,DID FROM dog WHERE UID = %s AND gender != %s", (
                uid, result[7])
        )
        currentUserDogs = cur.fetchall()
        cur.close()
        return render_template('dogprofile.html', currentAvatar=curAvatSrc, dog=result, dogImg=dogPicture, ownerImg=ownerPicture, traits=traitNames, curUserDogs=currentUserDogs)

    if request.method == 'POST':

        puppy = request.form
        reqDID = puppy['requestDog']
        uid = session['uid']

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT DID FROM dog WHERE name = %s AND UID = %s", (
                reqDID, uid
            )
        )
        reqId = cur.fetchone()
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM mating_request WHERE REQ_DID = %s AND REC_DID = %s", (
                reqId[0], int(dogid)
            )
        )
        exists = cur.fetchone()
        cur.close()

        if exists is None:
            time = datetime.now()
            dt_string = time.strftime("%Y-%m-%d")

            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO mating_request(REQ_DID, REC_DID, date_created, scheduled, completed) VALUES (%s,%s,%s,FALSE,FALSE)", (
                    reqId[0], int(dogid), dt_string
                )
            )
            mysql.connection.commit()
            cur.close()
            return redirect('/explore')

        else:
            flash("You have already sent mating request to this dog")
            return redirect("/dog/"+dogid)


@app.route('/requests', methods=['GET', 'POST'])
@flask_login.login_required
def requests():
    if request.method == 'GET':
        avatSrc = session['avatSrc']
        user = session['uid']
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM dog WHERE UID = %s", (
                user,
            )
        )
        result = cur.fetchall()

        cur.close()
        return render_template('mydogs.html', currentAvatar=avatSrc, dogs=result)


@app.route('/mydog/<dogid>/requests', methods=['GET', 'POST'])
@flask_login.login_required
def myDogRequests(dogid):
    if request.method == 'GET':

        avatSrc = session['avatSrc']

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM dog WHERE DID = %s", (
                dogid,
            )
        )
        result = cur.fetchone()
        dogSrc = result[5]
        cur.close()

        if session['uid'] == result[6]:

            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT * FROM dog d INNER JOIN mating_request m ON d.DID = m.REQ_DID INNER JOIN traits t ON t.TID = d.TID WHERE REC_DID = %s and scheduled=FALSE", (
                    dogid,
                )
            )
            requests = cur.fetchall()
            traitNames = ['PLAYFULL', 'CURIOUS', 'SOCIAL', 'AGGRESSIVE',
                          'DEMANDING', 'DOMINANT', 'PROTECTIVE', 'APARTMENT', 'VOCAL']
            return render_template('dogrequests.html', currentAvatar=avatSrc, dogData=result, dogImg=dogSrc, requestsData=requests, traits=traitNames)
        else:
            return redirect("/home")

    if request.method == 'POST':
        requestData = request.form
        id = requestData['id']
        type = requestData['requestType']

        if type == "accept":
            cur = mysql.connection.cursor()
            cur.execute(
                "UPDATE mating_request SET scheduled=TRUE WHERE REQ_DID=%s AND REC_DID=%s", (
                    int(id), dogid
                )
            )
            mysql.connection.commit()
            cur.close()
            return redirect("/mydog/"+dogid+"/scheduled")

        else:

            cur = mysql.connection.cursor()
            cur.execute(
                "DELETE FROM mating_request WHERE REQ_DID=%s AND REC_DID=%s", (
                    int(id), dogid
                )
            )
            mysql.connection.commit()
            cur.close()
            return redirect("/mydog/"+dogid+"/requests")

        return redirect("/home")


@app.route('/mydog/<dogid>/scheduled', methods=['GET', 'POST'])
@flask_login.login_required
def scheduledRequest(dogid):
    if request.method == 'GET':
        avatSrc = session['avatSrc']

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM dog WHERE DID = %s", (
                dogid,
            )
        )
        result = cur.fetchone()
        dogSrc = result[5]
        print(result[6])
        cur.close()

        if session['uid'] == result[6]:
            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT * FROM dog d INNER JOIN mating_request m ON d.DID = m.REQ_DID INNER JOIN traits t ON t.TID = d.TID WHERE REC_DID = %s and scheduled=TRUE", (
                    dogid,
                )
            )
            requests = cur.fetchall()
            traitNames = ['PLAYFULL', 'CURIOUS', 'SOCIAL', 'AGGRESSIVE',
                          'DEMANDING', 'DOMINANT', 'PROTECTIVE', 'APARTMENT', 'VOCAL']
            cur.close()
            return render_template('scheduledrequest.html', currentAvatar=avatSrc, dogData=result, dogImg=dogSrc, requestsData=requests, traits=traitNames)
        else:
            return redirect("/home")

    if request.method == 'POST':
        requestData = request.form
        id = requestData['id']
        cur = mysql.connection.cursor()
        cur.execute(
            "DELETE FROM mating_request WHERE REQ_DID=%s AND REC_DID=%s", (
                int(id), dogid
            )
        )
        mysql.connection.commit()
        cur.close()
        return redirect("/mydog/"+dogid+"/scheduled")


@app.route('/user/<userid>', methods=['GET'])
@flask_login.login_required
def userProfile(userid):
    if request.method == 'GET':

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT u.UID, u.username, u.img_src, a.street_and_num, a.city, a.country FROM user u INNER JOIN address a ON u.AID=a.AID WHERE UID=%s", (
                userid,
            )
        )
        result = cur.fetchone()
        cur.close()
        print(result)

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM dog d INNER JOIN traits t ON d.TID=t.TID WHERE d.UID=%s", (
                userid,
            )
        )
        dogData = cur.fetchall()
        cur.close()
        print(dogData)
        traitNames = ['PLAYFULL', 'CURIOUS', 'SOCIAL', 'AGGRESSIVE',
                      'DEMANDING', 'DOMINANT', 'PROTECTIVE', 'APARTMENT', 'VOCAL']

        return render_template('userprofile.html', currentAvatar=session['avatSrc'], userData=result, dogs=dogData, traits=traitNames)


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect("/")
