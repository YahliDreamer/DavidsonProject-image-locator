from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func
db = SQLAlchemy()

def get_appearance_stats_by_year(user_id):
    return db.session.query(
        func.year(Detection.timestamp),
        func.count()
    ).filter_by(user_id=user_id).group_by(func.year(Detection.timestamp)).all()

def get_top_websites(user_id, limit=10):
    return db.session.query(
        Detection.website_url,
        func.count()
    ).filter_by(user_id=user_id).group_by(Detection.website_url).order_by(func.count().desc()).limit(limit).all()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.Text)
    monitor_enabled = db.Column(db.Boolean, default=True)

class Detection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_url = db.Column(db.String(500))
    website_url = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

def save_detection(user_id, image_url, website_url):
    new_detection = Detection(user_id=user_id, image_url=image_url, website_url=website_url)
    db.session.add(new_detection)
    db.session.commit()

def get_all_users():
    return User.query.all()
