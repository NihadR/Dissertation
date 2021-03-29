from flask import render_template, flash, redirect, url_for, request, Blueprint
from dissertation import db
from dissertation.models import Topic
from flask_login import  login_required
from dissertation.admin.forms import TopicForm
import json

admin = Blueprint('admin', __name__)


@admin.route('/create_task', methods=['GET', 'POST'])
@login_required
def createtask():
    form = TopicForm()
    if form.validate_on_submit():
        option = request.form.get('options')
        random_string = f'''{form.content.data}'''
        encoded_string = json.dumps(random_string)
        task = Topic(title=form.title.data, description=form.description.data, content=encoded_string,
                     question_type=option, answer=form.answer.data)
        db.session.add(task)
        db.session.commit()
        flash('The task has been created', 'success')
        return redirect(url_for('admin.createtask'))
    return render_template('admin/create_task.html', title='Create Task', form=form)


@admin.route('/view_topics')
@login_required
def view_topics():
    topics = Topic.query.all()
    return render_template('admin/view_topics.html', topics=topics)


@admin.route('/view_topics/<int:topic_id>')
@login_required
def topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    return render_template('admin/topic.html', title=topic.title, topic=topic)


@admin.route('/view_topics/<int:topic_id>/update', methods=['GET', 'POST'])
@login_required
def update_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    form = TopicForm()
    if form.validate_on_submit():
        topic.title = form.title.data
        topic.content = form.content.data
        topic.answer = form.answer.data
        topic.description = form.description.data
        db.session.commit()
        flash('Topic has been updated', 'success')
        return redirect(url_for('admin.topic', topic_id=topic_id))
    elif request.method == 'GET':
        form.title.data = topic.title
        form.content.data = topic.content
        form.answer.data = topic.answer
        form.description.data = topic.description
    return render_template('admin/update_task.html', title='Update Task', form=form)





# @admin.route('/admin', methods=['GET', 'POST'])
# @login_required
# def admin():
#     return render_template('admin.html', title='Admin')



