from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/details", methods=["POST"])
def details():
    name = request.form.get('name')
    return render_template('details.html', name=name)
