from dissertation import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_login import UserMixin
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    '''
    Loads a user with the user id retrived from the User model
    '''
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    '''
    Creates the user table in the database with each line representing a different 
    column in the database 
    '''
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
    attempts = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, unique=False, default=False)
    courses = db.relationship('Course', backref='student_id', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        '''
        Creates a token for password reset 
        '''
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        '''
        Checks whether the token is valid or expired
        '''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        '''
        Returns the information from the User table when called in this format
        '''
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.test_taken}', '{self.pretest_result}' , '{self.learning_style_test_taken}', '{self.learning_style}', '{self.strengths}', '{self.weaknesses}')"


class Topic(db.Model):
    '''
    Creates the user table in the database with each line representing a different 
    column in the database 
    '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.Text, nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    learning_type = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        '''
        Returns the information from the Topic table when called in this format
        '''
        return f"Topic('{self.id}', '{self.title}', '{self.description}', '{self.content}', '{self.question_type}', '{self.answer}', '{self.learning_type}')"


class Course(db.Model):
    '''
    Creates the Course table in the database with each line repsenting a different 
    column
    '''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_list = db.Column(db.Text, nullable=False)

    def __repr__(self):
        '''
        Returns the information from the Course table when called in this format
        '''
        return f"Course('{self.user_id}', '{self.task_list}')"

