import os 

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('DB_USER')
    MAIL_PASSWORD = os.environ.get('DB_PASS')


    #     SECRET_KEY = os.environ.get'Mm0OTWLEtJYVmtX0PT3C8Uh2FxJ3eu0O'
    # SQLALCHEMY_DATABASE_URI = os.environ.get'sqlite:///site.db' 