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
import webbrowser
import matplotlib
# GUI.py
import customtkinter as ctk
import requests
from tkinter import filedialog
import matplotlib.pyplot as plt
  # Force safe backend for embedded use
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use("Agg")
import threading
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
        passwd = self.password_entry.get()

        response = requests.post("http://localhost:5000/auth/login", data={
            "email": email,
            "password": passwd
        })

        if response.status_code == 200:
            print("✅ Login successful!")
            user_data = response.json()
            print("📦 user_data received in GUI:", user_data)
            self.master.show_home(user_data=response.json())  # Pass user info to home
            #  Extract the access_token separately
            self.master.access_token = user_data["access_token"]
            self.master.user_id = user_data["user_id"]  # Optional if you use it

            self.master.show_home(user_data=response.json())
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
        self.label = ctk.CTkLabel(self, text="Welcome!", font=ctk.CTkFont(size=18, weight="bold"))

        self.label.pack(pady=10)

        # 🔍 Search bar
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(self, textvariable=self.search_var, placeholder_text="Search detections...", height=40, width=400, font=ctk.CTkFont(size=14))
        self.search_entry.pack(pady=(0, 10))
        self.search_entry.bind("<Return>", lambda event: self.load_detections())

        ctk.CTkButton(self, text="📊 View Reports", command=master.show_report).pack(pady=10)
        # ✅ Create scrollable frame to hold detection links
        self.scrollable_container = ctk.CTkScrollableFrame(self, width=550, height=450)
        self.scrollable_container.pack(padx=20, pady=10, fill="both", expand=True)


    def set_user_data(self, user_data):
        self.label.configure(text=f"Welcome, user ID: {user_data.get('user_id')}!")
        self.access_token = user_data['access_token']
        self.after(100, self.load_detections)

    def load_detections(self):
        keyword = self.search_var.get().lower().strip()
        try:
            response = requests.get(
                "http://localhost:5000/user/detections?limit=50",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            if response.status_code == 200:
                detections = response.json()
                # Filter by keyword
                if keyword:
                    detections = [d for d in detections if keyword in d["website_url"].lower()]

                for widget in self.scrollable_container.winfo_children():
                    widget.destroy()

                if not detections:
                    ctk.CTkLabel(self.scrollable_container, text="No detections found.").pack(pady=10)
                    return

                for det in detections:
                    website = det["website_url"]
                    timestamp = det.get("timestamp", "Unknown")

                    wrapper = ctk.CTkFrame(self.scrollable_container)
                    wrapper.pack(fill="x", pady=5, padx=10)

                    # Website button
                    link_btn = ctk.CTkButton(
                        wrapper,
                        text=website,
                        text_color="lightblue",
                        fg_color="transparent",
                        hover_color="#444",
                        anchor="w",
                        command=lambda url=website: webbrowser.open(url)
                    )
                    link_btn.pack(side="left", fill="x", expand=True)

                    # Timestamp label
                    ctk.CTkLabel(wrapper, text=f"🕓 {timestamp}", font=("Arial", 10)).pack(side="right")

            else:
                print("❌ Failed to load detections:", response.text)
        except Exception as e:
            print("❌ Exception while loading detections:", e)

    def open_link(self, url):
        import webbrowser
        webbrowser.open(url)

    def load_filtered_detections(self):
        keyword = self.search_entry.get().lower()
        self.load_detections(filter_keyword=keyword)

class ReportFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.label = ctk.CTkLabel(self, text="📊 Analytics Dashboard", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=10)

        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(fill="both", expand=True)

        self.email_toggle = ctk.CTkSwitch(self, text="📧 Email Alerts")
        self.sms_toggle = ctk.CTkSwitch(self, text="📱 SMS Alerts")
        self.email_toggle.pack(side="left", padx=20, pady=10)
        self.sms_toggle.pack(side="left", padx=20, pady=10)

        self.after(500, self.load_graphs)  # ✅ safe

    def load_graphs(self):
        try:
            response = requests.get("http://localhost:5000/user/report", headers={
                "Authorization": f"Bearer {self.master.access_token}"
            })

            if response.status_code == 200:
                data = response.json()
                self.display_graphs(data)
            else:
                ctk.CTkLabel(self.canvas_frame, text="❌ Failed to load report").pack()

        except Exception as e:
            ctk.CTkLabel(self.canvas_frame, text=f"❌ Error: {e}").pack()

    def display_graphs(self, data):
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import matplotlib.pyplot as plt

        # 🔁 Clear old content
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig_bar = Figure(figsize=(6, 4))
        ax_bar = fig_bar.add_subplot(111)
        websites = list(data['top_websites'].keys())
        counts = list(data['top_websites'].values())
        ax_bar.barh(websites, counts)
        ax_bar.set_title("Top Websites by Detections")
        ax_bar.set_xlabel("Detections")
        ax_bar.invert_yaxis()

        fig_line = Figure(figsize=(6, 4))
        ax_line = fig_line.add_subplot(111)
        ax_line.plot(data['trend_years'], data['trend_counts'], marker='o')
        ax_line.set_title("Detection Trends by Year")
        ax_line.set_xlabel("Year")
        ax_line.set_ylabel("Count")

        fig_pie = Figure(figsize=(5, 5))
        ax_pie = fig_pie.add_subplot(111)
        ax_pie.pie(counts, labels=websites, autopct="%1.1f%%")
        ax_pie.set_title("Detections by Platform")

        for fig in [fig_bar, fig_line, fig_pie]:
            chart = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            chart.get_tk_widget().pack(pady=10)
            chart.draw()
            trend_msg = data.get("trend_text", "")
            if trend_msg:
                ctk.CTkLabel(self.canvas_frame, text=f"📈 {trend_msg}", font=("Arial", 12)).pack(pady=5)

#  4. App Main GUI
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Face Recognition GUI")
        self.geometry("600x600")

        self.login_frame = LoginFrame(self)
        self.signup_frame = SignUpFrame(self)
        self.home_frame = HomeFrame(self)
        self.reports_frame = ReportFrame(self)

        self.show_login()

    def show_login(self):
        self.signup_frame.pack_forget()
        self.home_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

    def show_signup(self):
        self.login_frame.pack_forget()
        self.home_frame.pack_forget()
        self.signup_frame.pack(fill="both", expand=True)

    def show_report(self):
        self.login_frame.pack_forget()
        self.signup_frame.pack_forget()
        self.home_frame.pack_forget()
        self.reports_frame.pack(fill="both", expand=True)
        self.reports_frame.load_graphs()

    def show_home(self, user_data):
        self.login_frame.pack_forget()
        self.signup_frame.pack_forget()
        self.home_frame.set_user_data(user_data)

        self.home_frame.pack(fill="both", expand=True)

