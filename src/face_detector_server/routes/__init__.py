from .auth import auth_bp
from .detection import user_bp


def init_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    #creating a path connected to the root. which can be reached  by calling a function raped in a \auth
    app.register_blueprint(user_bp, url_prefix="/user")
