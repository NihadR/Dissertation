from dissertation import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    test_taken = db.Column(db.Boolean, unique=False, default=False)
    pretest_result = db.Column(db.String(60), nullable=True)
    learning_style_test_taken = db.Column(
        db.Boolean, unique=False, default=False)
    learning_style = db.Column(db.String(20), nullable=True)
    strengths = db.Column(db.String(60), nullable=True)
    weaknesses = db.Column(db.String(60), nullable=True)
    courses = db.relationship('Course', backref='student_id', lazy=True)
    bnmodels = db.relationship('BNModel', backref='student_id', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.test_taken}', '{self.pretest_result}' , '{self.learning_style_test_taken}', '{self.learning_style}', '{self.strengths}', '{self.weaknesses}')"


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Topic('{self.title}', '{self.description}', '{self.content}', '{self.question_type}', '{self.answer}')"


class BNModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"BNModel('{self.user_id}')"


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_list = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Course('{self.user_id}', '{self.task_list}')"


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Admin('{self.id}', '{self.email}')"
