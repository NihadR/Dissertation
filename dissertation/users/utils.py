from flask_mail import Message
from dissertation import  mail, db
from flask import url_for
from dissertation.models import User, Topic, Course
from flask_login import current_user
import ast
import random
import json

def gen_task_list(weaknesses):
    '''
    Takes a list of weaknesses and loops through them returning all tasks of that question_type
    Then randomly selects a task id and returns it in a task list 
    '''
    tasklist = []
    for i in weaknesses:
        task = Topic.query.filter_by(question_type=i).all()
        length = len(task)
        # Checks whether the amount of tasks is one if so returns that
        if length == 1:
            taskid = task[0]
            tasklist.append(taskid.id)
        else:
        # Takes a random task from the returned tasks from the list
            rand = random.randint(1, length)
            taskid = task[rand-1]
            tasklist.append(taskid.id)
    return tasklist


def pretest_analysis(df):
    '''
    Takes a dataframe with the user results from the pretest and analyses by checking whether
    the state prediction is greater than 0.8 
    '''
    statement = df['state_predictions'].iloc[0]
    ifstatement = df['state_predictions'].iloc[1]
    forloop = df['state_predictions'].iloc[2]
    strengths = []
    weaknesses = []
    if statement < 0.8:
        weaknesses.append('statement')
    else:
        strengths.append('statement')
    if ifstatement < 0.8:
        weaknesses.append('ifstatement')
    else:
        strengths.append('ifstatement')
    if forloop < 0.8:
        weaknesses.append('forloop')
    else:
        strengths.append('forloop')
    # Converts the list to a string for database input 
    stren = ''.join(strengths)
    weak = ''.join(weaknesses)
    # Generates a task list and creates a course for the student 
    tasklist = gen_task_list(weaknesses)
    course = Course(student_id=current_user, task_list=str(tasklist))
    # Updates the users strengths and wekanesses
    current_user.strengths = stren
    current_user.weaknesses = weak
    db.session.add(course)
    db.session.commit()




def get_course():
    '''
    Gets the course from the database and finds the related topics, constructes it in a dictionary
    format and returns in a list
    '''
    course = Course.query.filter_by(user_id=current_user.id).first()
    print(course)
    questions = []
    if not course:
        return questions
    else:
        # ast is used to remove the surrounding string 
        strtask = course.task_list
        x = ast.literal_eval(strtask)
        task = []
        for i in x:
            t = Topic.query.filter_by(id=i).first()
            task.append(t)

        for i in task:
            # Goes through each task and creates a dictionary under the relevant keys
            dic = {}
            dic['id'] = str(i.id)
            dic['title'] = i.title
            toStr = json.loads(i.content)
            answers = ast.literal_eval(toStr)
            dic['content'] = answers
            dic['description'] = i.description
            dic['answer'] = i.answer
            dic['question_type'] = i.question_type
            questions.append(dic)

    return questions

def content_analysis(df, list, length):
    '''
    Gets the answers from the user and generates a new course, if needed, for them
    Checks the state predictions and appends to a new list and then updates the 
    users strengths and weaknesses as well as generating the new relevant informaiton
    such as course
    '''
    statement = df['state_predictions'].iloc[0]
    all_types = ['statement', 'ifstatement', 'forloop']
    val = length/2
    strengths = []
    weaknesses = []
    course = Course.query.filter_by(user_id=current_user.id).first()
    db.session.delete(course)
    db.session.commit()
    # Checks the length of the list that was passed through to know how many questions the user answered 
    if val == 1:
        state = (list[1], df['state_predictions'].iloc[0])
        if state[1] < 0.55:
            weaknesses.append(state[0])
        else:
            strengths.append(state[0])
    elif val == 2:
        ifstatement = df['state_predictions'].iloc[1]
        state = (list[1], df['state_predictions'].iloc[0])
        state1 = (list[3], df['state_predictions'].iloc[1])
        if state[1] < 0.55:
            weaknesses.append(state[0])
        else:
            strengths.append(state[0])
        if state1[1] < 0.55:
            weaknesses.append(state1[0])
        else:
            strengths.append(state1[0])
    else:
        ifstatement = df['state_predictions'].iloc[1]
        forloop = df['state_predictions'].iloc[2]
        state = (list[1], df['state_predictions'].iloc[0])
        state1 = (list[3], df['state_predictions'].iloc[1])
        state2 = (list[5], df['state_predictions'].iloc[1])
        if state[1] < 0.55:
            weaknesses.append(state[0])
        else:
            strengths.append(state[0])
        if state1[1] < 0.55:
            weaknesses.append(state1[0])
        else:
            strengths.append(state1[0])
        if state2[1] < 0.55:
            weaknesses.append(state2[0])
        else:
            strengths.append(state2[0])
    print('wektype', type(weaknesses))
    print(weaknesses)
    # new_stren = list(set(all_types) - set(weaknesses))

    # Checks against the original questions to see what strengths the user has
    new_stren = [item for item in all_types if item not in weaknesses]
    current_user.strengths = ''.join(new_stren)

    # if not strengths:
    #     pass
    # elif not current_user.strengths:
    #     current_user.strengths = current_user.strengths.join(strengths)
    #     print('ifstatementsadnasdpasd', current_user.strengths)
    # else:
    #     current_strengths = current_user.strengths
    #     cs = ast.literal_eval(current_strengths)
    #     print('hi', cs)
    #     print('type', type(cs))
    #     temp = [item for item in strengths if item not in current_strengths]
    #     temp2 = current_strengths + temp
    #     stren = ''.join(temp2)
    #     current_user.strengths = stren
    #     print('asdknaspdaspdkasp', current_user.strengths)
    weak = ''.join(weaknesses)
    # Checks whether the weaknesses is empty if so a new tasklist is not needed 
    if not weaknesses:
        course = Course(student_id=current_user, task_list='')
        current_user.weaknesses = weak
        db.session.add(course)
        db.session.commit()
        print('hi', current_user.strengths)
    else:
        tasklist = gen_task_list(weaknesses)
        print(tasklist)
        course = Course(student_id=current_user, task_list=str(tasklist))
        current_user.weaknesses = weak
        db.session.add(course)
        db.session.commit()
        print('hihihihihihi', current_user.strengths)
    # strengths is '[]' remove the string to get the list and loop through and update

def send_reset_email(user):
    '''
    Takes a parameter of the user object 
    Constructs the msg with the unique link and send the email to the user
    '''
    token = user.get_reset_token()
    msg = Message('Password Reset Reqest', 
            sender='noreply@demo.com', 
            recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, ignore this email.
'''
    mail.send(msg)

