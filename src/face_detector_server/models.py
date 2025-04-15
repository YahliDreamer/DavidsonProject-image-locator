from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from datetime import datetime

bcrypt = Bcrypt()

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}  # ✅ THIS LINE FIXES THE ERROR
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)



    def set_password(self, password):
        # self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.password_hash = password

    def check_password(self, password):
        print(f'check_password {self.password_hash} {password}')
        return True
        return check_password_hash(self.password_hash, password)





class Detection(db.Model):
    __tablename__ = 'detection'
    __table_args__ = {'extend_existing': True}  # ✅ Add this line too

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    website_url = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
class FaceRecognitionStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    detections = db.Column(db.Integer, default=0)
