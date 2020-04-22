import os
import hashlib
from flask import session
from flask_session import Session
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, render_template, request, redirect, url_for
from models import User
from datetime import datetime
import logging

app = Flask(__name__)


# # Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
logging.basicConfig(filename='log.log', level=logging.DEBUG)


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(bind=engine))
db = db_session()


@app.route("/", methods=["GET", "POST"])
def index():
    # name = "Welcome to Books Ville. Please continue to login."
    if request.method == "GET":
        if session.get('data') is not None:
            return render_template("details.html", name=session.get('data'))
    return render_template("index.html")


@app.route("/auth", methods=["POST"])
def auth():
    uname = request.form['email']
    pwd = request.form['password']
    hashed_pwd = hashlib.md5(pwd.encode()).hexdigest()

    users = db.query(User).get(uname)

    if users is not None:
        if((uname == users.email) and (hashed_pwd == users.pswd)):
            session['data'] = uname
            return render_template("details.html", name=users.name.capitalize())
        else:
            return render_template('index.html', name="Incorrect Credentials. Please try again.")
    return render_template("index.html", name="You are not registered. Please click on Register Here.")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        session["data"] = []
        name = request.form['name']
        session["data"].append(name)

        email = request.form['email']
        session["data"].append(email.lower())

        is_user_present = db.execute("SELECT * FROM users WHERE email = :email",
                                     {"email": email}).fetchone()

        if is_user_present is not None:
            return render_template("index.html", name="Already a user. Please Log in to continue.")

        password = request.form['password']
        hashed_pwd1 = hashlib.md5(password.encode()).hexdigest()
        session["data"].append(hashed_pwd1)

        password2 = request.form['password2']
        hashed_pwd2 = hashlib.md5(password2.encode()).hexdigest()
        session["data"].append(hashed_pwd2)

        dob = request.form['dob']
        session["data"].append(dob)

        if hashed_pwd1 == hashed_pwd2:

            try:
                user = User(email=email, name=name,
                            pswd=hashed_pwd1, dob=dob, timestamp=datetime.now())
                db.add(user)

            except:
                return render_template("index.html", name="Something went wrong. Please Try Again.")

            db.commit()
            return render_template("index.html", name="You are now a member of Books Ville. Please log in to continue.")
        else:
            return render_template("index.html", name="Passwords mismatch please register again")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route("/admin", methods=["GET"])
def admin():
    users = db.query(User).order_by(desc(User.timestamp))
    return render_template("admin.html", users=users)


@app.route("/details", methods=["POST"])
def details():
    name = request.form.get('name')
    return render_template('details.html', name=name)
