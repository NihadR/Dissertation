# Dissertation

To create the conda environment

- conda create --name disso --file requirements.txt
- conda activate disso

1. This project was made in a conda environment
2. Debug mode
   export FLASK_DEBUG=1

3. To run server
   export FLASK_APP=run.py
   flask run

from dissertation import db, create_app
db.create_all(app=create_app())
db.drop_all(app=create_app())

Student Account

email: nihad1999@hotmail.co.uk
password:testing

Admin Account

email:testing@company.com
password:testing
