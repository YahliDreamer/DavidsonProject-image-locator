import threading
from src.face_detector_client.main import start_gui
from src.face_detector_server.main import start_server

if __name__ == '__main__':
        # ✅ Start the GUI in a separate thread
        threading.Thread(target=start_gui, daemon=True).start()

        # ✅ Start Flask server
        start_server()
