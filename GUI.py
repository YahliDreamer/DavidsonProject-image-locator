import customtkinter as ctk
import threading
from face_monitor import start_monitoring
import requests
# this 5 lines were added while trouble shouting.
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from database import db
# GUI.py
import customtkinter as ctk
import requests
from tkinter import filedialog

import customtkinter as ctk
from tkinter import filedialog
import requests

# db = SQLAlchemy()
bcrypt = Bcrypt()
# 1. Login Frame
class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Email").pack()
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.pack()

        ctk.CTkLabel(self, text="Password").pack()
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack()

        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=10)
        ctk.CTkButton(self, text="Sign Up", command=master.show_signup).pack()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        response = requests.post("http://localhost:5000/auth/login", data={
            "email": email,
            "password": password
        })

        if response.status_code == 200:
            print("✅ Login successful!")
            self.master.show_home(user_data=response.json())  # Pass user info to home
        else:
            print("❌ Login failed:", response.text)


# 2. Sign Up Frame
class SignUpFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Name").pack()
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack()

        ctk.CTkLabel(self, text="Email").pack()
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.pack()

        ctk.CTkLabel(self, text="Password").pack()
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack()

        ctk.CTkLabel(self, text="Phone").pack()
        self.phone_entry = ctk.CTkEntry(self)
        self.phone_entry.pack()

        self.image_path = ""
        ctk.CTkButton(self, text="Upload Image", command=self.upload_image).pack()

        ctk.CTkButton(self, text="Submit", command=self.signup).pack(pady=10)
        ctk.CTkButton(self, text="Back to Login", command=master.show_login).pack()

    def upload_image(self):
        path = filedialog.askopenfilename()
        self.image_path = path

    def signup(self):
        data = {
            "username": self.name_entry.get(),
            "email": self.email_entry.get(),
            "password": self.password_entry.get(),
            "phone": self.phone_entry.get()
        }

        if not self.image_path:
            print("❌ Please upload an image.")
            return

        try:
            with open(self.image_path, "rb") as img_file:
                files = {"image": img_file}
                response = requests.post("http://localhost:5000/auth/register", data=data, files=files)

            if response.status_code == 201:
                print("✅ Registered successfully!")
                self.master.show_login()
            else:
                print("❌ Registration failed:", response.text)
        except Exception as e:
            print(f"❌ Error during registration: {e}")


# 3. Home Frame (SQL stats, image results, etc.)
class HomeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.label = ctk.CTkLabel(self, text="Welcome! Stats coming soon.")
        self.label.pack(pady=20)

    def set_user_data(self, user_data):
        # Update this to fetch stats/images from your database
        self.label.configure(text=f"Welcome, {user_data.get('username', 'User')}!")


# 4. App Main GUI
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Face Recognition GUI")
        self.geometry("600x600")

        self.login_frame = LoginFrame(self)
        self.signup_frame = SignUpFrame(self)
        self.home_frame = HomeFrame(self)

        self.show_login()

    def show_login(self):
        self.signup_frame.pack_forget()
        self.home_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

    def show_signup(self):
        self.login_frame.pack_forget()
        self.home_frame.pack_forget()
        self.signup_frame.pack(fill="both", expand=True)

    def show_home(self, user_data):
        self.login_frame.pack_forget()
        self.signup_frame.pack_forget()
        self.home_frame.set_user_data(user_data)
        self.home_frame.pack(fill="both", expand=True)


# class App(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.title("Face Recognition Monitoring")
#         self.geometry("500x400")
#         self.create_widgets()
#
#     def create_widgets(self):
#         self.label = ctk.CTkLabel(self, text="Face Recognition App")
#         self.label.pack(pady=20)
#
#         self.start_button = ctk.CTkButton(self, text="Start Monitoring", command=self.start_monitoring)
#         self.start_button.pack(pady=10)
#
#     def start_monitoring(self):
#         threading.Thread(target=start_monitoring, daemon=True).start()
#         print("Monitoring started!")
#
#
# if __name__ == "__main__":
#     app = App()
#     app.mainloop()