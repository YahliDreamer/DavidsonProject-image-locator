
from src.face_detector_server.face_recognition.reverse_search import reverse_image_search
from src.face_detector_server.database import save_detection


def monitor_once(app, user):
    with app.app_context():
        print(" monitor_once called")
        print(f" User image URL: {user['image_url']}")
        if not user['monitor_enabled']:
            print(" monitor disabled")
            return
        print(f" Starting monitoring for: {user['email']}")
        results = reverse_image_search(user['image_url'])

        for result in results:
            print(f" Saving detection: {result}")
            save_detection(user['id'], "image", result.get("link"))



def start_monitoring(app, user):
    # while True: #todo fix useless loop
    monitor_once(app, user)


def start_monitoring_thread(app, user):
    import threading
    thread = threading.Thread(target=start_monitoring, args=(app, user), daemon=True)
    thread.start()
