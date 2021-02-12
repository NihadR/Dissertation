from flask import Flask, render_template, flash, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Mm0OTWLEtJYVmtX0PT3C8Uh2FxJ3eu0O'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    pretest_result = db.Column(db.Integer, nullable=True)
    courses = db.relationship('Course', backref='student_id', lazy=True)
    bnmodels = db.relationship('BNModel', backref='student_id', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.username}', '{self.pretest_result}')"


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_postedd = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    coursetopics = db.relationship('Course', backref='task_names', lazy=True)

    def __repr__(self):
        return f"Topic('{self.title}', '{self.description}', '{self.content}'"


class BNModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"BNModel('{self.user_id}'"


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_list = db.Column(db.Text, nullable=False)
    task_id = db.Column(
        db.String(120), db.ForeignKey('topic.id'), nullable=False)

    def __repr__(self):
        return f"Topic('{self.user_id}', '{self.task_list}', '{self.task_id}'"


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='login', form=form)


if __name__ == '__main':
    app.run(debug=True)
