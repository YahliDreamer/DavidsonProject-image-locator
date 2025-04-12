import time
import threading
from flask import Flask
from reverse_search import reverse_image_search
from database import get_all_users, save_detection
import random
import mysql.connector
from datetime import datetime
# next lines logic


def monitor_once(app):
    with app.app_context():
        from database import get_all_users, save_detection
        from reverse_search import reverse_image_search
        # ✅ ensure Flask context
        users = get_all_users()
        for user in users:
            if not user.monitor_enabled:
                continue  # 🔁 Skip users who disabled monitoring
            results = reverse_image_search(user.image_url)
            for result in results:
                save_detection(user.id, result.get("image"), result.get("link"))
                print(f"✅ Detection for {user.username}: {result.get('link')}")

#
# def monitor_once(app):
#     with app.app_context():
#         from database import get_all_users, save_detection
#         from reverse_search import reverse_image_search
#         # ✅ ensure Flask context
#         users = get_all_users()
#         for user in users:
#             if not user.monitor_enabled:
#                 continue  # 🔁 Skip users who disabled monitoring
#             results = reverse_image_search(user.image_url)
#             for result in results:
#                 save_detection(user.id, result.get("image"), result.get("link"))
#                 print(f"✅ Detection for {user.username}: {result.get('link')}")

def start_monitoring(app,user):
    import time
    while True:
        monitor_once(app,user)
        time.sleep(3600)

def start_monitoring_thread(app,user):
    import threading
    thread = threading.Thread(target=start_monitoring, args=(app,user), daemon=True)

    thread.start()