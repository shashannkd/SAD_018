import os
import hashlib
from flask import session
from flask_session import Session
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import User, Book
# from flask_json import FLASK_JSON, JsonError, json_response, as_json
from datetime import datetime
import logging

app = Flask(__name__)

# # Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# FlaskJSON(app)
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
            return render_template("details.html", name=session['data'])
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


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html", data=[{'field': 'ISBN'}, {'field': 'Title'}, {'field': 'Author'}, {'field': 'Year'}])
    elif request.method == "POST":
        s = ""
        select = request.form.get('comp')
        req = request.form.get('search')
        like_format = '%{}%'.format(req)
        if req == "":
            return render_template("search.html", msg="Search query cannot be empty")
        else:
            if select == "ISBN":
                stat = db.query(Book).filter(Book.isbn.like(
                    like_format)).order_by(Book.title).all()
            elif select == "Title":
                stat = db.query(Book).filter(
                    Book.title.like(like_format)).order_by(Book.title).all()
            elif select == "Author":
                stat = db.query(Book).filter(
                    Book.author.like(like_format)).order_by(Book.title).all()
            else:
                stat = db.query(Book).filter(Book.year.like(
                    like_format)).order_by(Book.title).all()
                # db.query(Book).order_by(desc(User.time))
            # stat=sorted(stat,)
            if len(stat) == 0:
                return render_template("noresult.html")
            else:
                return render_template("results.html", stat=stat)


@app.route("/api/search", methods=["POST"])
def api_search():
    #     if request.method == "GET":
    #         return render_template("search.html", data=[{'field': 'ISBN'}, {'field': 'Title'}, {'field': 'Author'}, {'field': 'Year'}])
    #     else:
    #         data = request.get_json()
    #         try:
    #             select = data["comp"]
    #             req = data["search"]
    #             print(str(select)+str(req))
    #         except:
    #             print("aszdxf")


@app.route("/book/<string:isbn>")
def bookdetails(isbn):
    return render_template("isbnvar.html", isbn=isbn)
