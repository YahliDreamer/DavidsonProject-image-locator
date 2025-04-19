from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended import jwt_required, get_jwt_identity
import threading
from database import db
from models import User, Detection
from auth import authenticate_user, register_user, auth_bp  # Import authentication routes
from reverse_search import reverse_image_search
from notifications import send_alert
from GUI import App
import customtkinter as ctk
import tkinter as tk
from PIL import Image
import requests
import datetime
from auth import authenticate_user, register_user,auth_bp  # Import your auth blueprint
# from models import User  # Import your User model

from flask_sqlalchemy import SQLAlchemy
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Shailta1055Yahli5510.@localhost/face_recognition'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Change this in production

db.init_app(app)
login_manager = LoginManager(app)
jwt = JWTManager(app)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/user/detections', methods=['GET'])
@jwt_required()
def get_detections():
    user_id = get_jwt_identity()
    limit = request.args.get('limit', default=5, type=int)

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid user ID"}), 400

    detections = Detection.query.filter_by(user_id=user_id) \
        .order_by(Detection.timestamp.desc()) \
        .limit(limit) \
        .all()

    data = [
        {
            'website_url': d.website_url,
            'image_url': d.image_url,
            'timestamp': d.timestamp.strftime('%Y-%m-%d %H:%M:%S') if d.timestamp else "Unknown"
        }
        for d in detections
    ]

    return jsonify(data)
# @app.route('/user/detections')
# @jwt_required()
# def get_detections():
#     user_id = get_jwt_identity()
#     detections = Detection.query.filter_by(user_id=user_id).all()
#     data = [{'website_url': d.website_url, 'image_url': d.image_url} for d in detections]
#     return jsonify(data)
#

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp, url_prefix='/auth')  # Register authentication module
with app.app_context():
    db.create_all()


# **📌 User Registration**

# **📌 Homepage - Display User's Online Presence**
@app.route('/home')
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
        new_detection = Detection(user_id=current_user.id, image_url=result['image'], website_url=result['link'])
        db.session.add(new_detection)
        send_alert(current_user, result['link'])

    db.session.commit()
    return redirect(url_for('home'))

@app.route('/user/report')
@jwt_required()
def report():
    from sqlalchemy import func
    from collections import defaultdict
    import datetime

    user_id = get_jwt_identity()

    # 🔢 Count by website
    top_sites = db.session.query(
        Detection.website_url, func.count().label("count")
    ).filter_by(user_id=user_id).group_by(Detection.website_url).order_by(func.count().desc()).limit(5).all()

    top_websites = {site: count for site, count in top_sites}

    # 📊 Count detections by year (for trend chart)
    detections = Detection.query.filter_by(user_id=user_id).order_by(Detection.timestamp.desc()).limit(200).all()

    year_counts = defaultdict(int)
    for det in detections:
        if det.timestamp:
            year = det.timestamp.year
            year_counts[year] += 1

    MAX_YEARS = 10
    trend_years = sorted(year_counts)[-MAX_YEARS:]  # Get the last MAX_YEARS
    trend_counts = [year_counts[y] for y in trend_years]

    # 🗓️ Also calculate this_year vs last_year
    current_year = datetime.datetime.now().year
    last_year = current_year - 1

    this_year_count = year_counts.get(current_year, 0)
    last_year_count = year_counts.get(last_year, 0)

    # 📈 Text summary
    if last_year_count:
        change = this_year_count - last_year_count
        trend_text = f"You appeared {abs(change)}× {'more' if change > 0 else 'less'} this year than last year!"
    else:
        trend_text = "Not enough data to compare year-over-year."

    return jsonify({
        "top_websites": top_websites,
        "this_year": this_year_count,
        "last_year": last_year_count,
        "trend_text": trend_text,
        "trend_years": trend_years,
        "trend_counts": trend_counts
    })

# **📌 Secure Logout**
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Global variable to track if the GUI is already running
gui_running = False

def start_gui():
    global gui_running
    if not gui_running:  # Check if the GUI is already running
        gui_running = True
        app = App()
        app.mainloop()

@app.route('/user/stats', methods=['GET'])
@jwt_required()
def get_stats():
    user_id = get_jwt_identity()

    from database import get_appearance_stats_by_year, get_top_websites

    yearly = get_appearance_stats_by_year(user_id)
    top_sites = get_top_websites(user_id)

    return jsonify({
        "yearly": [{"year": y[0], "count": y[1]} for y in yearly],
        "top_sites": [{"site": s[0], "count": s[1]} for s in top_sites]
    })


if __name__ == '__main__':
        # ✅ Start the face monitoring background thread
        # from face_monitor import start_monitoring_thread
        #
        # start_monitoring_thread(app)

        # ✅ Start the GUI in a separate thread
        threading.Thread(target=start_gui, daemon=True).start()

        # ✅ Start Flask server
        app.run(debug=True, use_reloader=False)  # Prevents Flask from running twice
    # # Start the GUI in a separate thread
    # threading.Thread(target=start_gui, daemon=True).start()
    # # Run the Flask app
    # app.run(debug=True, use_reloader=False)  # Prevents Flask from running twice
    #
