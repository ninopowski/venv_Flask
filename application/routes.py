from application import app, db
from application.models import User, Course, Enrollment
from application.forms import LoginFrom, RegisterForm
from flask import render_template, request, Response, redirect, url_for, flash, session
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
    # checking if the user is signed in
    if not session.get('username'):
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    courseID = request.form.get("courseID")
    course_title = request.form.get("title")
    term = request.form.get("term")

    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"You are already registerd in {course_title}.", "danger")
            return redirect(url_for('courses'))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(f"You enrolled to {course_title}.", "success")
    classes = list(User.objects.aggregate(*[
            {
                '$lookup': {
                    'from': 'enrollment',
                    'localField': 'user_id',
                    'foreignField': 'user_id',
                    'as': 'result'
                }
            }, {
                '$unwind': {
                    'path': '$result',
                    'includeArrayIndex': 'result_id',
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$lookup': {
                    'from': 'course',
                    'localField': 'result.courseID',
                    'foreignField': 'courseID',
                    'as': 'result2'
                }
            }, {
                '$unwind': {
                    'path': '$result2',
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$match': {
                    'user_id': user_id
                }
            }, {
                '$sort': {
                    'courseID': 1
                }
            }
        ]))
    return render_template("enrollment.html", enrollment=True, title="Enrollment", classes=classes)

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
    # checking if user is already signed in
    if session.get('username'):
        return redirect(url_for('index'))
    form = LoginFrom()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user:
            if user.check_password(password):
                flash(f"{user.first_name}, you are successfully logged in.", "success")
                session['user_id'] = user.user_id
                session['username'] = user.first_name
                return redirect(url_for('index'))
            else:
                flash("Wrong password, try again.", "danger")
                return redirect(url_for('login'))
        else:
            flash("Something went wrong.", "danger")
    return render_template("login.html", form=form, title="Login", login=True)

@app.route("/logout")
def logout():
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('index'))


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