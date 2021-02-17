from flask import render_template, flash, redirect, url_for, request
from dissertation import app, db, bcrypt
from dissertation.forms import RegistrationForm, LoginForm, UpdateAccForm
from dissertation.models import User, Topic, BNModel, Course
from flask_login import login_user, current_user, logout_user, login_required
from collections import Counter


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


questions = {
    'How do you best revise?': ['Through the use of diagrams', 'Through the use of videos and lectures',
                                'Through notes and reading material', 'Through participating in practicals'],
    "What's the best way for you to learn something new?": ['Through charts', 'Watching a video about it',
                                                            'Reading a book about it', 'Figuring it out on your own'],
    "In a new country how would you find your way around?": ['Using a map', 'Using the internet',
                                                             'Read an atlas', 'Walk around till you find your destination'],
    "What kind of book do you like to read": ["A book with images", "Audio book", "A novel", "Book with crosswords"],
    "What do you think about exams?": ['Would prefer if they have more diagram based questions', 'Would prefer more oral questions',
                                       'I like them', 'Would prefer more practical assessments'],
    "How do you solve problems": ["Visualising the problem", "Thinking out loud", "Through writing the problem down",
                                  "Thinking about while exercising"]
}
questions3 = {
    "What do you like to do relax?": ['Read', 'Listen to music', 'Exercise'],
    "In what setting do you learn the best": ['Study group', 'Study session by yourself', 'Field Trips'],
    "Can you memorise song lyrics after listening to it a few times?": ['Yes, I can memorise it easily', 'No, I need to read the song lyrics',
                                                                        "No, but I prefer dancing to it"],
    "Do you find youself needing to take frequent breaks when studying or restless during a lecture": ['No, I like it', 'Yes, its too much reading for me ', 'Yes, I would like more practical based material']
}


@app.route('/learning_style', methods=['GET', 'POST'])
@login_required
def learning_style():
    if request.method == 'POST':
        print('hi')
        learningstyle = []
        for i in questions.keys():
            answered = request.form[i]
            if questions[i][0] == answered:
                learningstyle.append('A')
            elif questions[i][1] == answered:
                learningstyle.append('B')
            elif questions[i][2] == answered:
                learningstyle.append('C')
            else:
                learningstyle.append('D')
        for i in questions3.keys():
            answered = request.form[i]
            if questions3[i][0] == answered:
                learningstyle.append('A')
                learningstyle.append('B')
            elif questions3[i][1] == answered:
                learningstyle.append('C')
            else:
                learningstyle.append('D')
        print(learningstyle)
        ans = Counter(learningstyle)
        ans = ans.most_common(1)[0][0]
        print('ans', ans)

    return render_template('lstyle.html',  q=questions, q3=questions3)
