from flask import render_template, request, Blueprint
from dissertation.algorithm import runmodel

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    # runmodel()
    return render_template('main/home.html')


@main.route('/about')
def about():
    return render_template('main/about.html')