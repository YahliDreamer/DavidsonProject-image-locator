import os

UPLOAD_FOLDER = 'static/uploads'


class Config:
    SECRET_KEY = os.urandom(24)
    UPLOAD_FOLDER = UPLOAD_FOLDER
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost/world'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'super-secret-key'  # Change this in production
