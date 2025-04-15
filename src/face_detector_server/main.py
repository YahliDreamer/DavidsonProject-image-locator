from src.face_detector_server import create_app


def start_server():
    app = create_app()
    app.run(debug=True, use_reloader=False)  # Prevents Flask from running twice


if __name__ == '__main__':
    start_server()
