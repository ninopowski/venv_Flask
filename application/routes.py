from application import app, db
from application.models import User, Course, Enrollment
from application.forms import LoginFrom, RegisterForm
from flask import render_template, request, Response, redirect, url_for, flash
import json


@app.route("/")
@app.route("/index")
def index():
    login = False
    return render_template("index.html", login=login, index=True)

@app.route("/courses")
@app.route("/courses/<term>")
def courses(term = None):
    if term is None:
        term = "Winter 2023"
    classes = Course.objects.all()
    print(classes)
    return render_template("courses.html", data=classes, courses=True, term=term)

@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    id = request.form.get("courseID")
    title = request.form.get("title")
    term = request.form.get("term")
    return render_template("enrollment.html", data={"id":id, "title":title, "term":term})

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count() + 1
        password = form.password_two.data
        user = User()
        user.user_id = user_id
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.set_password(password)
        user.save()
        flash("You are registered", "success")
        return redirect(url_for('index'))
    return render_template("register.html", form=form, register=True)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user:
            if user.check_password(password):
                flash(f"{user.first_name}, you are successfully logged in.", "success")
                return redirect(url_for('index'))
            else:
                flash("Wrong password, try again.", "danger")
                return redirect(url_for('login'))
        else:
            flash("Something went wrong.", "danger")
    return render_template("login.html", form=form, title="Login", login=True)

@app.route("/api/")
@app.route("/api/<idx>")
def api(idx = None):
    if(idx == None):
        #print(idx)
        jdata = data_json
    else:
        print(idx)
        jdata = data_json[int(idx)]

    return Response(json.dumps(jdata), mimetype="application/json")

@app.route("/user")
def user():
    #User(user_id=1, first_name="Nino", last_name="Perkovikj", email="nino@mail.com", password="username").save()
    #User(user_id=2, first_name="Mary", last_name="Jane", email="m.jane@mail.com", password="1234").save()
    users = User.objects.all()
    return render_template("user.html", users=users)