import time
import threading
from flask import Flask
from reverse_search import reverse_image_search
from database import get_all_users


from database import save_detection  # Ensure this function stores results in the database

def start_monitoring():
    from main import app
    while True:
        with app.app_context():  # ✅ מבטיח שהקוד ירוץ בתוך ההקשר של Flask
            users = get_all_users()
            for user in users:
                results = reverse_image_search(user.image_url)
                for result in results:
                    save_detection(user.id, result["image"], result["link"])
                    print(f"New detection for {user.username}: {result['link']}")

        time.sleep(3600)  # בדיקה כל שעה

def start_monitoring_thread():
    thread = threading.Thread(target=start_monitoring, daemon=True)
    thread.start()
