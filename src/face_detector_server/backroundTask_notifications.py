# background_tasks/notifications.py
from threading import Thread
import time
from src.face_detector_server.models import User, Detection
from src.face_detector_server.extensions import db
from src.face_detector_server.face_recognition.reverse_search import reverse_image_search
from src.face_detector_server.routes.notifications import send_email_alert, send_alert

def run_notifications(app):
    with app.app_context():
        while True:
            users = User.query.filter((User.notify_email == True) | (User.notify_sms == True)).all()
            for user in users:
                results = reverse_image_search(user.image_url)
                new_links = [link for link in results if link not in [d.url for d in user.detections]]

                for link in new_links:
                    detection = Detection(user_id=user.id, url=link)
                    db.session.add(detection)

                    if user.notify_email:
                        send_email_alert(user.email, "New face appearance!", f"🔍 Your face was found at: {link}")
                    if user.notify_sms and user.phone_number:
                        send_alert(user.phone_number, f"Your face was found: {link}")

                db.session.commit()

            time.sleep(86400)  # 24 שעות
