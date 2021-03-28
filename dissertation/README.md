# Dissertation

1. This project was made in a conda environment
1. Debug mode
   export FLASK_DEBUG=1

1. To run server
   export FLASK_APP=run.py
   flask run

from dissertation import db

db.create_all()

from dissertation.models import User
User.query.first()

1. To create superadmin
   from dissertation import db
   from dissertation.models import Admin
   from flask_bcrypt import Bcrypt
   bcrypt = Bcrypt()
   hashed_password = bcrypt.generate_password_hash('testing').decode('utf-8')
   admin = Admin(email = 'nihad1999@hotmail.co.uk', password = hashed_password)
   db.session.add(admin)
   db.session.commit()

Stuff to do

fix key error bug on content page

do the about page content, look into compiler if not then do online ide

add something to homepage

do dashboard button points

do is_admin and make sure pages have correct accesss

check strengths to see if it is being added

REFACTOR
