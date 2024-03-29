import os 

class Config:
    '''
    Holds all the information regarding the system 
    Including sensitive information such as the secret key 
    and email and password which are locally stored 
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('DB_USER')
    MAIL_PASSWORD = os.environ.get('DB_PASS')