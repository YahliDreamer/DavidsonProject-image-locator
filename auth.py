from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import db, User  # Ensure User model is imported
from flask_bcrypt import Bcrypt
auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()
from werkzeug.utils import secure_filename
import os

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def register_user(username, email, password):
    """
    Registers a new user and stores their hashed password in the database.
    """
    if User.query.filter_by(email=email).first():
        return None  # Email is already registered

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return new_user  # Return the newly created user


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    API endpoint to register a new user.
    """
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user = register_user(username, email, password)

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
    data = request.json
    email = data.get('email')
    password = data.get('password')

    token = authenticate_user(email, password)

    if token:
        return jsonify({'access_token': token}), 200
    return jsonify({'error': 'Invalid email or password'}), 401
