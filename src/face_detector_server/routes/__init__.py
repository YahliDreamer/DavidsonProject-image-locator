from .auth import auth_bp


def init_routes(app):
    app.register_blueprint(auth_bp)
