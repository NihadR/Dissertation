from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from dissertation import db, bcrypt
from dissertation.algorithm import predictmodel
from dissertation.users.testquestions import questions, lsquestions, lsquestions3
from dissertation.users.forms import RegistrationForm, LoginForm, UpdateAccForm, RequestResetForm, ResetPasswordForm
from dissertation.models import User, Topic, Course
from dissertation.users.utils import pretest_analysis, gen_task_list,get_course,content_analysis,send_reset_email
import pandas as pd
import json
import time
from datetime import datetime
from statistics import mode

users = Blueprint('users', __name__)

var = 0
@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password, test_taken=False, pretest_result=0, is_admin=False)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect(url_for('users.login'))
    return render_template('user/register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login Successful', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('user/login.html', title='login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account information has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('user/account.html', title='acount', form=form)


@users.route('/dashboard')
@login_required
def dashboard():
    return render_template('user/dashboard.html')


@users.route('/test', methods=['GET', 'POST'])
@login_required
def take_test():
    return render_template('user/test.html', title='Pretest')

@users.route('/learning_style', methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))

    return render_template('user/lstyle.html',  q=questions, q3=questions3)


@users.route('/pretest', methods=['GET', 'POST'])
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
        return redirect(url_for('main.home'))
    return render_template('user/pretest.html',  q=question)

@users.route('/content', methods=['GET', 'POST'])
def content():
    questions = get_course()
    global var
    if var == 0:
        var = datetime.now()

    if request.method == 'POST':
        endtime = datetime.now()
        testanswers = []
        for i in questions:
            print(i)
            print('answer', i.get('answer'))
            print('id', request.form[i.get('id')])
            if request.form[i.get('id')] == i.get('answer'):
                testanswers.append(1)
                testanswers.append(i['question_type'])
            else:
                testanswers.append(0)
                testanswers.append(i['question_type'])
        length = len(testanswers)
        print(testanswers)
        if length/2 == 1:
            df = pd.DataFrame({'user_id': [current_user.id],
                               'skill_name': [testanswers[1]],
                               'correct': [testanswers[0]]})
        elif length/2 == 2:
            df = pd.DataFrame({'user_id': [current_user.id, current_user.id],
                               'skill_name': [testanswers[1], testanswers[3]],
                               'correct': [testanswers[0], testanswers[2]]})
        else:
            df = pd.DataFrame({'user_id': [current_user.id, current_user.id, current_user.id],
                               'skill_name': [testanswers[1], testanswers[3], testanswers[5]],
                               'correct': [testanswers[0], testanswers[2], testanswers[4]]})
        pred = predictmodel(df)
        print('content', pred)
        content_analysis(pred, testanswers, length)
    return render_template('user/content.html', q=questions)

@users.route('/compiler')
def compiler():
    return render_template('user/ide.html')

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('user/reset_request.html', form=form, title="Reset Password")


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been reset', 'success')
        return redirect(url_for('users.login'))
    return render_template('user/reset_token.html', form=form, title="Reset Password")
