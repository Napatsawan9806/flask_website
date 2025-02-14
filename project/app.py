from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"


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
    print(request.method)
    if request.method == "POST":
        if request.form.get("login") == "Login":
            print("login")
            return redirect(url_for("home"))
        else:
            return render_template("login.html")
    else:
        pass
    return render_template("login.html")


@app.route("/sign_in", methods=["POST", "GET"])
def signin():
    return render_template("signin.html")


if __name__ == "__main__":
    app.run(debug=True)
