from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    print(request.method)
    if request.method == "POST":
        if request.form.get("login") == "Login":
            print("login")
            return redirect(url_for("login"))
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


if __name__ == "__main__":
    app.run(debug=True)
