from flask import Flask
from src.face_detector_server.extensions import db, login_manager, jwt
from src.face_detector_server.config import Config
from src.face_detector_server.models import User
from src.face_detector_server.routes import init_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()

    login_manager.init_app(app)
    jwt.init_app(app)

    # Set user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register routes
    init_routes(app)

    return app



