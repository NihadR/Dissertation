from flask import render_template, flash, redirect, url_for, request
from dissertation import app, db, bcrypt, mail
from dissertation.forms import (RegistrationForm, LoginForm, UpdateAccForm, AdminLoginForm,
                                TopicForm, RequestResetForm, ResetPasswordForm)
from dissertation.models import User, Topic, BNModel, Course, Admin
from flask_login import login_user, current_user, logout_user, login_required
# from collections import Counter
# from statistics import mode
# from dissertation.testquestions import questions, lsquestions, lsquestions3
# from dissertation.algorithm import runmodel, predictmodel
# from flask_mail import Message
# import pandas as pd
# import json
# import time
# import random
# import ast
# from datetime import datetime

var = 0

















