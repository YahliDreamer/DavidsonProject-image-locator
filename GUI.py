import customtkinter as ctk
import threading
from face_monitor import start_monitoring


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Face Recognition Monitoring")
        self.geometry("500x400")
        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Face Recognition App")
        self.label.pack(pady=20)

        self.start_button = ctk.CTkButton(self, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(pady=10)

    def start_monitoring(self):
        threading.Thread(target=start_monitoring, daemon=True).start()
        print("Monitoring started!")


if __name__ == "__main__":
    app = App()
    app.mainloop()