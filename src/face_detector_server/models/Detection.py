from datetime import datetime
from src.face_detector_server.extensions import db


class Detection(db.Model):
    __tablename__ = 'detection'
    __table_args__ = {'extend_existing': True}  # ✅ Add this line too

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    website_url = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
