import os
from flask import current_app, Blueprint, request, jsonify, redirect, url_for
from flask_jwt_extended import create_access_token
from flask_login import logout_user, login_required
from flask_bcrypt import generate_password_hash
from werkzeug.utils import secure_filename

from src.face_detector_server.config import UPLOAD_FOLDER
from src.face_detector_server.models import User
from src.face_detector_server import db
from src.face_detector_server.face_recognition.face_monitor import start_monitoring_thread

auth_bp = Blueprint('auth', __name__)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    API endpoint to register a new user.
    """
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    phone_number = request.form.get('phone_number')
    notify_email = request.form.get('notify_email') == '1'
    notify_sms = request.form.get('notify_sms') == '1'
    image = request.files.get('image')

    #  Save the image to disk
    image_url = None  # todo check why not used

    if image:
        filename = secure_filename(image.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image.save(filepath)
        image_url = filepath
    else:
        return jsonify({'error': 'No image uploaded'}), 400

    user: User or None = register_user(
        name=username,
        email=email,
        password=password,
        image_url=image_url,
        phone_number=phone_number,
        notify_email=notify_email,
        notify_sms=notify_sms
    )

    if user:
        user_data = dict(image_url=user.image_url, monitor_enabled=user.monitor_enabled, email=user.email, id=user.id)
        #  Start background face monitoring
        try:
            start_monitoring_thread(current_app._get_current_object(), user_data)
            print(f" Monitoring started for {user.email}")
        except Exception as e:
            print(f" Error starting monitoring: {e}")

        return jsonify({'message': 'User registered successfully'}), 201

    return jsonify({'error': 'Email already exists'}), 400


@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        # generate new token to identify user session
        access_token = create_access_token(identity=str(user.id))  #  force to string

        return jsonify({
            'access_token': access_token,
            'user_id': user.id,
            'username': user.username,
            'image_url': user.image_url
        }), 200


    return jsonify({'error': 'Invalid email or password'}), 401



# ** Secure Logout**
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


def register_user(name, email, password, image_url, phone_number=None, notify_email=False, notify_sms=False) -> User or None:
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None  # User already exists

    #  Properly hash the password
    hashed_password = generate_password_hash(password)

    new_user = User(
        username=name,
        email=email,
        password_hash=hashed_password,
        image_url=image_url,
        phone_number=phone_number,
        notify_email=notify_email,
        notify_sms=notify_sms,
        monitor_enabled=True
    )
    # add new user to SQL database
    db.session.add(new_user)
    db.session.commit()

    return new_user
