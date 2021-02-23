from flask import render_template, flash, redirect, url_for, request
from dissertation import app, db, bcrypt
from dissertation.forms import RegistrationForm, LoginForm, UpdateAccForm
from dissertation.models import User, Topic, BNModel, Course
from flask_login import login_user, current_user, logout_user, login_required
from collections import Counter
from statistics import mode
from dissertation.testquestions import questions, lsquestions, lsquestions3
import re


@app.route('/')
@app.route('/home')
def home():
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
    # if request.method == 'POST':
    #     testanswers = []
    #     for i in question.keys():
    #         answered = request.form[i]

    #         # print('answres', answered.strip())
    #         # print('questio', questions[i][0].strip())
    #         if question[i][0] == answered:
    #             testanswers.append('1')
    #         else:
    #             testanswers.append('0')
    #     print(testanswers)
    # if request.method == 'POST':
    #     testanswers = []
    #     for q in questions:
    #         print(request.form[q.get('id')], q.get('correct'))
    #         # print('correct')
    #         if request.form[q.get('id')] == q.get('correct'):
    #             testanswers.append('0')
    #         else:
    #             testanswers.append('1')
    #     print(testanswers)
    if request.method == 'POST':
        testanswers = []
        for i in question:
            if request.form[i.get('id')] == i.get('correct'):
                testanswers.append('1')
            else:
                testanswers.append('0')
        print(testanswers)

    return render_template('pretest.html',  q=question)
# questions = [
#     {
#         "id" : 1,
#         "question" :" asobfbdosfj",
#         "answers" : {
#             '1' : "answer 1",
#             '2' :"answer 2"
#         },
#         "correct" : '1'

#     },
#     {
#         "id" : 2,
#         "question" :" asobfbdosfj",
#         "answers" : {
#             '1' : "answer 1",
#             '2' :"answer 2"
#         },
#         "correct" : '1'

#     }
# ]
# questions.answers.keys()
