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
    pretest_result = db.Column(db.Integer, nullable=True)
    courses = db.relationship('Course', backref='student_id', lazy=True)
    bnmodels = db.relationship('BNModel', backref='student_id', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.test_taken}', '{self.pretest_result}')"


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
