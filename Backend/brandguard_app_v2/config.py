import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    BASE_UPLOAD_FOLDER = '/home/muhammadmoizkhan/Music/flask_app/schedular_check/brandguard_app/refrence_images'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
