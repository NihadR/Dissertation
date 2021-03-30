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
   change user creation is_admin == True

Stuff to do

fix key error bug on content page

do the about page content, look into compiler if not then do online ide DONE

add something to homepage DONE
dissertation/models.py
do dashboard button points DONE

do is_admin and make sure pages have correct accesss
pages have been altered, recreate database and test DONE (remember to change back to true)
Perhaps change to 403 error page

check strengths to see if it is being added

REFACTOR DONE

Comments

Testing

from dissertation import db, create_app
db.create_all(app=create_app()) or
db.drop_all(app=create_app())
