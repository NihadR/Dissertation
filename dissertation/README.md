# Dissertation

1. This project was made in a conda environment
2. Debug mode
   export FLASK_DEBUG=1

3. To run server
   export FLASK_APP=run.py
   flask run

from dissertation import db, create_app
db.create_all(app=create_app())
db.drop_all(app=create_app())

Stuff to do

fix key error bug on content page DONE

do the about page content, look into compiler if not then do online ide DONE

add something to homepage DONE
do dashboard button points DONE

do is_admin and make sure pages have correct accesss DONE
pages have been altered, recreate database and test DONE (remember to change back to true)

check strengths to see if it is being added DONE

REFACTOR DONE

Comments DONE

Look into adding learning style type to questions and checking for it
Testing
