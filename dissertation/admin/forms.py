from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email


class TopicForm(FlaskForm):
    '''
    Topic form for creating or updating a task
    Validates the inputted data
    '''
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    answer = IntegerField('Answer', validators=[DataRequired()])
    submit = SubmitField('Add Task')


