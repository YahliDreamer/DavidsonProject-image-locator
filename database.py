from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

def save_detection(user_id, image_url, website_url):
    new_detection = Detection(user_id=user_id, image_url=image_url, website_url=website_url)
    db.session.add(new_detection)
    db.session.commit()

def get_all_users():
    return User.query.all()
