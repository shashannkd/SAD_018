from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/auth", methods=["POST"])
def auth():
    uname = request.form['uname']
    pwd = request.form['password']
    hashed_pwd = hashlib.md5(pwd.encode()).hexdigest()

    if uname.trim():
        return render_template('index.html', name="")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/details", methods=["POST"])
def details():
    name = request.form.get('name')
    return render_template('details.html', name=name)
