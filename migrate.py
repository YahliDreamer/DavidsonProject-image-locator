from flask_migrate import Migrate
from src.face_detector_server import create_app
from src.face_detector_server.extensions import db

app = create_app()
migrate = Migrate(app, db)
