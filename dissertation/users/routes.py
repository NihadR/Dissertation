from flask import render_template, flash, redirect, url_for, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from dissertation import db, bcrypt
from dissertation.algorithm import predictmodel
from dissertation.users.testquestions import questions, lsquestions, lsquestions3
from dissertation.users.info import infor
from dissertation.users.forms import RegistrationForm, LoginForm, UpdateAccForm, RequestResetForm, ResetPasswordForm
from dissertation.models import User, Topic, Course
from dissertation.users.utils import pretest_analysis, gen_task_list,get_course,content_analysis,send_reset_email
import pandas as pd
import json
import time
import traceback
import ast
from datetime import datetime
from statistics import mode

users = Blueprint('users', __name__)

var = 0
@users.route('/register', methods=['GET', 'POST'])
def register():
    '''
    Allows a user to register to the website
    Takes form input and creates a new user adding them to the database 
    Redirects them to the login page
    '''
    try:
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))
        form = RegistrationForm()
        if form.validate_on_submit():
            # Takes the submitted data and hashes the password and creates a new user with the remaing data
            # Commits to the database
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user = User(username=form.username.data,
                        email=form.email.data, password=hashed_password, test_taken=False, pretest_result=0, is_admin=False)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created', 'success')
            return redirect(url_for('users.login'))
    except Exception as e:
        traceback.print_exc()
        return abort(500)
    return render_template('user/register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Allows a user to login into the system 
    Takes email and password input and checks whether they exist in the system
    Uses the login_user function to login them in 
    Redirects them to the dashboard if successful
    '''
    try:
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                # Calls the login function and passes through the user to the flask login 
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash('Login Successful', 'success')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    except Exception as e:
        traceback.print_exc()
        return abort(500)
    return render_template('user/login.html', title='login', form=form)

@users.route('/logout')
def logout():
    '''
    Logs a user out of the system
    '''
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    '''
    Allows a user to view their username and email and update them if needed
    Updates these values if valid and commits the changes to the database
    '''
    try:
        form = UpdateAccForm()
        # Displays users strengths and weaknesses
        if not current_user.strengths:
            stren = current_user.strengths
        else:
            stren = ast.literal_eval(current_user.strengths)
        if not current_user.weaknesses:
            weak = current_user.weaknesses
        else:
            weak = ast.literal_eval(current_user.weaknesses)
        if form.validate_on_submit():
            # Gets the updated user details from the form and updates the database
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Account information has been updated', 'success')
            return redirect(url_for('users.account'))
        elif request.method == 'GET':
            # Displays current user information on the page 
            form.username.data = current_user.username
            form.email.data = current_user.email
    except Exception as e:
        traceback.print_exc()
        return abort(500)
    return render_template('user/account.html', title='acount', form=form, stren=stren, weak=weak)


@users.route('/dashboard')
@login_required
def dashboard():
    '''
    Route to act as a home page for all further actions by the user 
    '''
    return render_template('user/dashboard.html')

@users.route('/learning_style', methods=['GET', 'POST'])
@login_required
def learning_style():
    '''
    Takes user answers to input through POST request, checks the given answers which are mapped to 
    pre-defined learning styles and total the different types, taking the mode
    Update the users account and redirect them to the account page
    '''
    try:
        questions = lsquestions
        questions3 = lsquestions3
        if request.method == 'POST':
            learningstyle = []
            # Gets the keys from the dictionary and compares to the answered questions to check
            # which response and has given and appends to a new list
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
            # Mode is taken to return the learning style
            ans = mode(learningstyle)
            style = ''
            if ans == 'A':
                style = 'Visual'
            elif ans == 'B':
                style = 'Reading/Writing'
            elif ans == 'C':
                style = 'Auditory'
            else:
                style = 'Kinesthesis'

            # User information is updated
            current_user.learning_style = style
            current_user.learning_style_test_taken = True
            db.session.commit()
            flash('Learning Style results have been submitted', 'success')
            return redirect(url_for('users.account'))
    except Exception as e:
        traceback.print_exc()
        return abort(500)
    return render_template('user/lstyle.html',  q=questions, q3=questions3)


@users.route('/pretest', methods=['GET', 'POST'])
@login_required
def pretest():
    '''
    Creates the route with the question dictionary passed through to the template
    User input is taken and keys are matched with answers to calculate the user's score
    Transformed into a datafram and fed into the model 
    '''
    try:
        question = questions
        global var
        if var == 0:
            var = datetime.now()

        if request.method == 'POST':
            endtime = datetime.now()
            
            testanswers = []
            for i in question:
                # Gets the keys from the form and match them with correct answer
                if request.form[i.get('id')] == i.get('correct'):
                    testanswers.append(1)
                else:
                    testanswers.append(0)
            # Convert list to json to be stored in the database 
            # 
            ans = json.dumps(testanswers)
            current_user.test_taken = True
            current_user.pretest_result = ans
            db.session.commit()
            state, ifstate, forl = 0, 0, 0
            # Multiple questions regarding each topic so take either 1 or 0 depending
            # if they get both right
            if (testanswers[0] + testanswers[5])/2 == 1:
                state = 1
            if (testanswers[1] + testanswers[3])/2 == 1:
                ifstate = 1
            if (testanswers[2] + testanswers[4])/2 == 1:
                forl = 1


            # Creates the dataframe with the information processed above
            df = pd.DataFrame({'user_id': [current_user.id, current_user.id, current_user.id],
                            'skill_name': ['statement', 'ifstatement', 'forloop'],
                            'correct': [state, ifstate, forl],
                            'start_time': [var, var, var],
                            'end_time': [endtime, endtime, endtime]})

            # Calls the predict function on the dataframe to get the state prediction
            # Passes this through the dataframe to the pretest_analysis function
            pred = predictmodel(df)
            pretest_analysis(pred)
            flash('Pretest results have been submitted successfully', 'success')
            return redirect(url_for('main.home'))
    except Exception as e:
        traceback.print_exc()
        return abort(500)
    return render_template('user/pretest.html',  q=question)

@users.route('/content', methods=['GET', 'POST'])
def content():
    '''
    Displays the precribed tasks to the student and takes the input and analysis it

    Returns the user to the dashboard
    '''
    try:
        questions = get_course()
        global var
        if var == 0:
            var = datetime.now()
        if request.method == 'POST':
            endtime = datetime.now()
            testanswers = []

            # enumerated keys are processed to prevent keyerrors from dictionary 
            # checks whether the correct answer has been given and appends accordingly 
            for i in questions:
                k = f"""{i.get('id')}"""
                new_key = request.form[k]
                if new_key == i.get('answer'):
                    testanswers.append(1)
                    testanswers.append(i['question_type'])
                else:
                    testanswers.append(0)
                    testanswers.append(i['question_type'])

            length = len(testanswers)
        
            # Creates appropriate length dictionary according to the amount of questions the user was given
            if length/2 == 1:
                df = pd.DataFrame({'user_id': [current_user.id],
                                'skill_name': [testanswers[1]],
                                'correct': [testanswers[0]], 
                                'start_time': [var],
                                'end_time': [endtime]})
            elif length/2 == 2:
                df = pd.DataFrame({'user_id': [current_user.id, current_user.id],
                                'skill_name': [testanswers[1], testanswers[3]],
                                'correct': [testanswers[0], testanswers[2]],
                                    'start_time': [var, var],
                                'end_time': [endtime, endtime]})
            else:
                df = pd.DataFrame({'user_id': [current_user.id, current_user.id, current_user.id],
                                'skill_name': [testanswers[1], testanswers[3], testanswers[5]],
                                'correct': [testanswers[0], testanswers[2], testanswers[4]],
                                    'start_time': [var, var, var],
                                'end_time': [endtime, endtime, endtime]})
            # Calls predict function on the dataframe and passes the output to the be analysed further
            pred = predictmodel(df)
            print('content', pred)
            content_analysis(pred, testanswers, length)
            flash('Responses have been submitted successfully', 'success')
            return redirect(url_for('users.dashboard'))
    except Exception as e:
        traceback.print_exc()
        return abort(500)
    return render_template('user/content.html', q=questions, enumerate=enumerate)

@users.route('/compiler')
def compiler():
    '''
    Built-in IDE for the user to use 
    '''
    return render_template('user/ide.html')

@users.route('/info')
def info():
    '''
    Displays content for the user to understand the topics 
    '''
    information = infor
    return render_template('user/info.html', i = information)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    '''
    Checks whether inputs are valid and finds passes through the users email to the method 
    to generate password request 
    '''
    try:
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))
        form = RequestResetForm()
        if form.validate_on_submit():
            # Finds the user's account and calls the function to send the password request
            user = User.query.filter_by(email=form.email.data).first()
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('users.login'))
    except Exception as e:
        traceback.print_exc()
        return abort(500)
    return render_template('user/reset_request.html', form=form, title="Reset Password")


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    '''
    Route with the token for user to reset passed, checks whether token is still valid
    Allows user to then reset the password and commits the changes to the database 
    '''
    try:
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))
        user = User.verify_reset_token(token)
        if not user:
            flash('That is an invalid or expired token', 'warning')
            return redirect(url_for('users.reset_request'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            # Takes the new password and hashes it, commits it to the database
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been reset', 'success')
            return redirect(url_for('users.login'))
    except Exception as e:
        traceback.print_exc()
        return abort(500)
    return render_template('user/reset_token.html', form=form, title="Reset Password")
