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
from forms import RegisterForm, LoginForm
from models import db, User, bcrypt, Course, Enrollment
from decorators import admin_required


app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logout", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/dashboard/enroll", methods=["GET", "POST"])
@login_required
def enroll():
    courses = Course.query.all()  # ดึงรายชื่อวิชาทั้งหมดจากฐานข้อมูล
    if request.method == "POST":
        course_id = request.form.get("course")
        existing_enrollment = Enrollment.query.filter_by(
            user_id=current_user.id, course_id=course_id
        ).first()
        if not existing_enrollment:
            new_enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
            db.session.add(new_enrollment)
            db.session.commit()
            flash("ลงทะเบียนวิชาเรียบร้อย!", "success")
        else:
            flash("คุณได้ลงทะเบียนวิชานี้แล้ว!", "warning")
        return redirect(url_for("schedule"))
    return render_template("register_course.html", courses=courses)


@app.route("/dashboard/withdraw")
@login_required
def withdraw():
    return render_template("withdraw.html")


@app.route("/dashboard/schedule")
@login_required
def schedule():
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    return render_template("schedule.html", enrollments=enrollments)


@app.route("/admin/courses", methods=["GET", "POST"])
@login_required
@admin_required
def manage_courses():
    courses = Course.query.all()
    if request.method == "POST":
        course_name = request.form["name"]
        course_schedule = request.form["schedule"]
        new_course = Course(name=course_name, schedule=course_schedule)
        db.session.add(new_course)
        db.session.commit()
        flash("เพิ่มวิชาเรียบร้อย!", "success")
        return redirect(url_for("manage_courses"))
    return render_template("admin_courses.html", courses=courses)


@app.route("/admin/courses/delete/<int:course_id>", methods=["POST"])
@login_required
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash("ลบวิชาเรียบร้อย!", "success")
    return redirect(url_for("manage_courses"))


@app.route("/admin/courses/edit/<int:course_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    if request.method == "POST":
        course.name = request.form["name"]
        course.schedule = request.form["schedule"]
        db.session.commit()
        flash("แก้ไขวิชาเรียบร้อย!", "success")
        return redirect(url_for("manage_courses"))
    return render_template("edit_course.html", course=course)


@app.route("/", methods=["POST", "GET"])
def home():
    print(request.method)
    if request.method == "POST":
        if request.form.get("login") == "Login":
            print("login")
            return redirect(url_for("login"))
        elif request.form.get("register") == "Register":
            print("sign in")
            return redirect(url_for("register"))
        else:
            return render_template("home.html")
    else:
        pass
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
