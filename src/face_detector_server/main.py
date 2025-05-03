from src.face_detector_server import create_app
from src.face_detector_server.backroundTask_notifications import run_notifications
import threading
def start_server():
    app = create_app()
    # notification_thread = threading.Thread(target=run_notifications, args=(app,), daemon=True)
    # notification_thread.start()
    app.run(debug=True, use_reloader=False)  # Prevents Flask from running twice


if __name__ == '__main__':
    start_server()
