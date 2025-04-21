from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user

from src.face_detector_server.routes.notifications import send_alert
from src.face_detector_server.face_recognition.reverse_search import reverse_image_search
from src.face_detector_server import db
from src.face_detector_server.models import Detection


app = Blueprint('main', __name__)


# **📌 Homepage - Display User's Online Presence**
@app.route('/')
@login_required
def home():
    detections = Detection.query.filter_by(user_id=current_user.id).all()
    labels = [d.website_url for d in detections]
    values = [1] * len(detections)  # Each website is counted once

    return render_template('home.html', detections=detections, labels=labels, values=values)


# **📌 Reverse Image Search (Triggered on Login)**
@app.route('/search')
@login_required
def search():
    image_url = current_user.image_url
    results = reverse_image_search(image_url)

    for result in results:
        new_detection = Detection(user_id=current_user.id, image_url='image', website_url=result['link'])
        db.session.add(new_detection)
        send_alert(current_user, result['link'])

    db.session.commit()
    return redirect(url_for('home'))

