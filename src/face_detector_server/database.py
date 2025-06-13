from sqlalchemy import func

from src.face_detector_server import db
from src.face_detector_server.models.Detection import Detection
from src.face_detector_server.models.User import User


def get_appearance_stats_by_year(user_id):
    return db.session.query(
        func.year(Detection.timestamp),
        func.count()
    ).filter_by(user_id=user_id).group_by(func.year(Detection.timestamp)).all()


def get_top_websites(user_id, limit=5):
    return db.session.query(
        Detection.website_url,
        func.count()
    ).filter_by(user_id=user_id).group_by(Detection.website_url).order_by(func.count().desc()).limit(limit).all()


def save_detection(user_id, image_url, website_url):
    new_detection = Detection(user_id=user_id, image_url=image_url, website_url=website_url)
    db.session.add(new_detection)
    db.session.commit()
    print(f" Detection saved for user {user_id} to {website_url}")


def get_all_users():
    return User.query.all()
