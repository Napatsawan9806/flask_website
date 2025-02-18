from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin,
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash

import models
import forms

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

models.init_db(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "Login"


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


@app.route("/", methods=["POST", "GET"])
def home():
    print(request.method)
    if request.method == "POST":
        if request.form.get("login") == "Login":
            print("login")
            return redirect(url_for("login"))
        elif request.form.get("signin") == "Sign in":
            print("sign in")
            return redirect(url_for("signin"))
        else:
            return render_template("home.html")
    else:
        pass
    return render_template("home.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("login success")
            return redirect(url_for("home"))
        else:
            flash("login failed")
    return render_template("login.html", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        existing_user = models.User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("user already exists")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(form.password.data)
        new_user = models.User(username=form.username.data, password=hashed_password)
        models.db.session.add(new_user)
        models.db.session.commit()

        flash("Account created successful")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
