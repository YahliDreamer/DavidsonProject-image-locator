import os
from flask import current_app, Blueprint, request, jsonify, redirect, url_for
from flask_jwt_extended import create_access_token
from flask_login import logout_user, login_required
from flask_bcrypt import generate_password_hash
from werkzeug.utils import secure_filename

from src.face_detector_server.config import UPLOAD_FOLDER
from src.face_detector_server.models import User
from src.face_detector_server import db
# from face_monitor import start_monitoring_thread
from src.face_detector_server.face_recognition.face_monitor import start_monitoring_thread

auth_bp = Blueprint('auth', __name__)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    API endpoint to register a new user.
    """
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    image = request.files['image']
    # ✅ Save the image to disk
    image_url = None
    if image:
        filename = secure_filename(image.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image.save(filepath)
        image_url = filepath  # ✅ This is what should be saved in DB
    else:
        return jsonify({'error': 'No image uploaded'}), 400

    user = register_user(username, email, password, image_url)

    if user:
        return jsonify({'message': 'User registered successfully'}), 201
    return jsonify({'error': 'Email already exists'}), 400


@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))  # ✅ force to string
        # ✅ Start background face monitoring
        try:
            start_monitoring_thread(current_app._get_current_object(), user)
            print(f"[✅] Monitoring started for {user.email}")
        except Exception as e:
            print(f"[❌] Error starting monitoring: {e}")

        return jsonify({
            'access_token': access_token,
            'user_id': user.id,
            'username': user.username,
            'image_url': user.image_url
        }), 200


    return jsonify({'error': 'Invalid email or password'}), 401


# **📌 Secure Logout**
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


def register_user(name, email, password, image_url):
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None  # User already exists

    # ✅ Properly hash the password
    hashed_password = generate_password_hash(password)

    new_user = User(
        username=name,
        email=email,
        password_hash=hashed_password,
        image_url=image_url
    )
    db.session.add(new_user)
    db.session.commit()

    return new_user


def authenticate_user(email, password):
    """
    Authenticates a user by checking their email and password.
    Returns a JWT token if authentication is successful.
    """
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        return create_access_token(identity=user.id)  # Generate JWT token

    return None  # Authentication failed


