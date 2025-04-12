from models import User
from flask import Blueprint, request, jsonify
from database import db  # ✅ use same db instance!
from flask_jwt_extended import create_access_token
# from models import db, User  # Ensure User model is imported
from flask_bcrypt import Bcrypt
from flask_bcrypt import generate_password_hash
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
from face_monitor import start_monitoring_thread
from flask import current_app

import threading
auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


from werkzeug.security import generate_password_hash

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
def authenticate_user(email, password):
    """
    Authenticates a user by checking their email and password.
    Returns a JWT token if authentication is successful.
    """
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        return create_access_token(identity=user.id)  # Generate JWT token

    return None  # Authentication failed


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Handles user login by verifying credentials and returning a JWT token.
    """

    email = request.form['email']
    password = request.form['password']

    token = authenticate_user(email, password)

    if token:
        # ✅ Start face monitoring only for this session
        threading.Thread(target=start_monitoring_thread, args=(current_app._get_current_object(),), daemon=True).start()

        return jsonify({'access_token': token}), 200
    return jsonify({'error': 'Invalid email or password'}), 401
