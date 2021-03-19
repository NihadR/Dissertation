from flask import render_template, flash, redirect, url_for, request
from dissertation import app, db, bcrypt
from dissertation.forms import RegistrationForm, LoginForm, UpdateAccForm, AdminLoginForm, TopicForm
from dissertation.models import User, Topic, BNModel, Course, Admin
from flask_login import login_user, current_user, logout_user, login_required
from collections import Counter
from statistics import mode
from dissertation.testquestions import questions, lsquestions, lsquestions3
from dissertation.algorithm import runmodel, predictmodel
import pandas as pd
import json
import time
import random
from datetime import datetime

var = 0


@app.route('/')
@app.route('/home')
def home():
    runmodel()
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password, test_taken=False, pretest_result=0)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/create_task', methods=['GET', 'POST'])
@login_required
def createtask():
    form = TopicForm()
    if form.validate_on_submit():
        option = request.form.get('options')
        task = Topic(title=form.title.data, description=form.description.data, content=form.content.data,
                     question_type=option, answer=form.answer.data)
        db.session.add(task)
        db.session.commit()
        flash('The task has been created', 'success')
        return redirect(url_for('createtask'))
    return render_template('create_task.html', title='Create Task', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login Successful', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='login', form=form)


@app.route('/admin_login', methods=['GET', 'POST'])
def adminlogin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login Successful', 'success')
            return redirect(next_page) if next_page else redirect(url_for('admin'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('admin_login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account information has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='acount', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/test', methods=['GET', 'POST'])
@login_required
def take_test():
    return render_template('test.html', title='Pretest')


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template('admin.html', title='Admin')


@app.route('/learning_style', methods=['GET', 'POST'])
@login_required
def learning_style():
    questions = lsquestions
    questions3 = lsquestions3
    if request.method == 'POST':
        learningstyle = []
        for i in lsquestions.keys():
            answered = request.form[i]
            if lsquestions[i][0] == answered:
                learningstyle.append('A')
            elif lsquestions[i][1] == answered:
                learningstyle.append('B')
            elif lsquestions[i][2] == answered:
                learningstyle.append('C')
            else:
                learningstyle.append('D')
        for i in lsquestions3.keys():
            answered = request.form[i]
            if lsquestions3[i][0] == answered:
                learningstyle.append('A')
                learningstyle.append('B')
            elif lsquestions3[i][1] == answered:
                learningstyle.append('C')
            else:
                learningstyle.append('D')
        ans = mode(learningstyle)
        print(learningstyle)
        style = ''
        if ans == 'A':
            style = 'Visual'
        elif ans == 'B':
            style = 'Reading/Writing'
        elif ans == 'C':
            style = 'Auditory'
        else:
            style = 'Kinesthesis'

        current_user.learning_style = style
        current_user.learning_style_test_taken = True
        db.session.commit()
        flash('Learning Style results have been submitted', 'success')
        return redirect(url_for('account'))

    return render_template('lstyle.html',  q=questions, q3=questions3)


@app.route('/pretest', methods=['GET', 'POST'])
@login_required
def pretest():
    question = questions
    global var
    if var == 0:
        var = datetime.now()

    if request.method == 'POST':
        endtime = datetime.now()

        testanswers = []
        for i in question:
            if request.form[i.get('id')] == i.get('correct'):
                testanswers.append(1)
            else:
                testanswers.append(0)
        ans = json.dumps(testanswers)
        # print(type(ans))
        current_user.test_taken = True
        current_user.pretest_result = ans
        db.session.commit()
        state, ifstate, forl = 0, 0, 0
        if (testanswers[0] + testanswers[5])/2 == 1:
            state = 1
        if (testanswers[1] + testanswers[3])/2 == 1:
            ifstate = 1
        if (testanswers[2] + testanswers[4])/2 == 1:
            forl = 1

        # df = pd.DataFrame({'user_id': [current_user.id, current_user.id, current_user.id],
        #                    'skill_name': ['statement', 'ifstatement', 'forloop'],
        #                    'correct': [state, ifstate, forl],
        #                    'hints': [0, 0, 0], 'attempts': [1, 1, 1],
        #                    'start_time': [var, var, var],
        #                    'end_time': [endtime, endtime, endtime]})
        df = pd.DataFrame({'user_id': [current_user.id, current_user.id, current_user.id],
                           'skill_name': ['statement', 'ifstatement', 'forloop'],
                           'correct': [state, ifstate, forl]})
        print(df)
        pred = predictmodel(df)
        pretest_analysis(pred)
        return redirect(url_for('home'))
    return render_template('pretest.html',  q=question)


def pretest_analysis(df):
    statement = df['state_predictions'].iloc[0]
    ifstatement = df['state_predictions'].iloc[1]
    forloop = df['state_predictions'].iloc[2]
    strengths = []
    weaknesses = []
    if statement < 0.9:
        weaknesses.append('statement')
    else:
        strengths.append('statement')
    if ifstatement < 0.9:
        weaknesses.append('ifstatement')
    else:
        strengths.append('ifstatement')
    if forloop < 0.9:
        weaknesses.append('forloop')
    else:
        strengths.append('forloop')
    stren = ''.join(strengths)
    weak = ''.join(weaknesses)
    tasklist = gen_task_list(weaknesses)
    course = Course(student_id=current_user, task_list=str(tasklist))
    current_user.strengths = stren
    current_user.weaknesses = weak
    db.session.add(course)
    db.session.commit()


def gen_task_list(weaknesses):
    tasklist = []
    for i in weaknesses:
        task = Topic.query.filter_by(question_type=i).all()
        length = len(task)
        print('this', length)
        if length == 1:
            taskid = task[0]
            tasklist.append(taskid.id)
        else:
            rand = random.randint(0, length)
            print('rand', rand)
            taskid = task[rand]
            tasklist.append(taskid.id)
    return tasklist


@app.route('/content')
def content():
    course = Course.query.filter_by(user_id=current_user.id).first()
    tasklist = course.task_list
    for i in tasklist:
    print(tasklist)
    # if course = '':
    #     # do nothing
    # else:

    return render_template('content.html')


@app.route('/compiler')
def compiler():
    return render_template('testcompiler.html')
