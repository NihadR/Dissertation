from flask import render_template, flash, redirect, url_for, request, Blueprint, abort
from dissertation import db
from dissertation.models import Topic
from flask_login import  login_required, current_user
from dissertation.admin.forms import TopicForm
import json
import traceback

admin = Blueprint('admin', __name__)


@admin.route('/create_task', methods=['GET', 'POST'])
@login_required
def createtask():
    '''
    Allows admin to create a new task
    Creates the task and pushes it to database
    '''
    try:
        form = TopicForm()
        # Checks whether the user trying to access the page is an admin
        # if current_user.is_admin == False:
        #     abort(403)
        if form.validate_on_submit():
            # Gets the inputted data and creates the task 
            option = request.form.get('options')
            # Content is stored in a json format for the database
            random_string = f'''{form.content.data}'''
            encoded_string = json.dumps(random_string)
            task = Topic(title=form.title.data, description=form.description.data, content=encoded_string,
                        question_type=option, answer=form.answer.data)
            db.session.add(task)
            db.session.commit()
            flash('The task has been created', 'success')
            return redirect(url_for('admin.createtask'))
    except Exception as e:
        traceback.print_exc()
        return abort(500)
    return render_template('admin/create_task.html', title='Create Task', form=form)


@admin.route('/view_topics')
@login_required
def view_topics():
    '''
    Allows the admin to view all topics in the database
    '''
    # Checks whether the user trying to access the page is an admin
    # if current_user.is_admin == False:
    #     abort(403)
    try:
        topics = Topic.query.all()
    except Exception as e:
        traceback.print_exc()
        return abort(500)
    return render_template('admin/view_topics.html', topics=topics)


@admin.route('/view_topics/<int:topic_id>')
@login_required
def topic(topic_id):
    '''
    Allows the admin to view a single task, displaying more information 
    regarding that task
    '''
    # Checks whether the user trying to access the page is an admin
    # if current_user.is_admin == False:
    #     abort(403)
    try:
        topic = Topic.query.get_or_404(topic_id)
    except Exception as e:
        traceback.print_exc()
        return abort(500)
    return render_template('admin/topic.html', title=topic.title, topic=topic)


@admin.route('/view_topics/<int:topic_id>/update', methods=['GET', 'POST'])
@login_required
def update_topic(topic_id):
    '''
    Allows the admin to update a task 
    Takes the inputted data and updates a task 
    '''
    # Checks whether the user trying to access the page is an admin
    # if current_user.is_admin == False:
    #     abort(403)
    try:
        topic = Topic.query.get_or_404(topic_id)
        form = TopicForm()
        if form.validate_on_submit():
            # Takes the new data and updates it in the database
            topic.title = form.title.data
            topic.content = form.content.data
            topic.answer = form.answer.data
            topic.description = form.description.data
            db.session.commit()
            flash('Topic has been updated', 'success')
            return redirect(url_for('admin.topic', topic_id=topic_id))
        elif request.method == 'GET':
            # Displays the current information regarding that task on the page 
            form.title.data = topic.title
            form.content.data = topic.content
            form.answer.data = topic.answer
            form.description.data = topic.description
    except Exception as e:
        traceback.print_exc()
        return abort(500)
    return render_template('admin/update_task.html', title='Update Task', form=form)


@admin.route('/admin_dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    '''
    Dashboard template for the admin, allows them to navigate through 
    the different functions available to them 
    '''
    # Checks whether the user trying to access the page is an admin
    # if current_user.is_admin == False:
    #     abort(403)
    return render_template('admin/admin_dashboard.html', title='Admin')



