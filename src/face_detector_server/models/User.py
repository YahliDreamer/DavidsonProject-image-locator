from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import UserMixin

from src.face_detector_server import db
from sqlalchemy import Boolean

# from src.face_detector_server.extensions import db


class User(UserMixin,db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}  # ✅ THIS LINE FIXES THE ERROR
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    monitor_enabled = db.Column(Boolean, default=True)
    notify_email = db.Column(db.Boolean, default=False)
    notify_sms = db.Column(db.Boolean, default=False)
    phone_number = db.Column(db.String(20))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'