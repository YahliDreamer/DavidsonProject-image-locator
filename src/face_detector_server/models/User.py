from src.face_detector_server.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.Text)
    monitor_enabled = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.username}>'