from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import threading
from database import db, User, Detection
from auth import authenticate_user, register_user, auth_bp  # Import authentication routes
from reverse_search import reverse_image_search
from notifications import send_alert
from GUI import App
import customtkinter as ctk
import tkinter as tk
from PIL import Image
import requests
from auth import auth_bp  # Import your auth blueprint
from models import User  # Import your User model

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

@app.route('/user/detections')
@jwt_required()
def get_detections():
    user_id = get_jwt_identity()
    detections = Detection.query.filter_by(user_id=user_id).all()
    data = [{'website_url': d.website_url, 'image_url': d.image_url} for d in detections]
    return jsonify(data)


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



if __name__ == '__main__':
    # Start the GUI in a separate thread
    threading.Thread(target=start_gui, daemon=True).start()
    # Run the Flask app
    app.run(debug=True, use_reloader=False)  # Prevents Flask from running twice

