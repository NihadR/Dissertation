from flask import render_template, request, Blueprint
from dissertation.algorithm import runmodel

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    '''
    Home page 
    Runs the model when first landing on the page 
    '''
    runmodel()
    return render_template('main/home.html')


@main.route('/about')
def about():
    '''
    About page, renders a template providing information to the user 
    '''
    return render_template('main/about.html')