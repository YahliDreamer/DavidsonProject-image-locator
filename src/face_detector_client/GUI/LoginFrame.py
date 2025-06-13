import customtkinter as ctk
import requests

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        #  Set pink background
        self.configure(fg_color="#ffe6f0")  # Light pink

        #  Title label
        self.title_label = ctk.CTkLabel(
            self,
            text="Welcome Back 💖",
            font=("Comic Sans MS", 28, "bold"),
            text_color="#ff66b2"
        )
        self.title_label.pack(pady=(40, 20))

        # ️ Email label and entry
        self.email_label = ctk.CTkLabel(
            self,
            text="Email",
            font=("Comic Sans MS", 16, "bold"),
            text_color="#ff3399"
        )
        self.email_label.pack(pady=(10, 5))
        self.email_entry = ctk.CTkEntry(
            self,
            corner_radius=15,
            fg_color="#ffffff",
            text_color="#ff3399"
        )
        self.email_entry.pack(pady=(0, 20), ipadx=10, ipady=5)

        #  Password label and entry
        self.password_label = ctk.CTkLabel(
            self,
            text="Password",
            font=("Comic Sans MS", 16, "bold"),
            text_color="#ff3399"
        )
        self.password_label.pack(pady=(10, 5))
        self.password_entry = ctk.CTkEntry(
            self,
            show="*",
            corner_radius=15,
            fg_color="#ffffff",
            text_color="#ff3399"
        )
        self.password_entry.pack(pady=(0, 20), ipadx=10, ipady=5)

        #  Login button
        self.login_button = ctk.CTkButton(
            self,
            text="✨ Login ✨",
            command=self.login,
            fg_color="#ff66b2",
            hover_color="#ff99cc",
            corner_radius=20,
            font=("Comic Sans MS", 16, "bold")
        )
        self.login_button.pack(pady=(10, 10), ipadx=10, ipady=5)

        #  Sign up button
        self.signup_button = ctk.CTkButton(
            self,
            text="🎀 Sign Up 🎀",
            command=master.show_signup,
            fg_color="#ffffff",
            text_color="#ff66b2",
            border_color="#ff66b2",
            border_width=2,
            hover_color="#ffe6f0",
            corner_radius=20,
            font=("Comic Sans MS", 16, "bold")
        )
        self.signup_button.pack(pady=(0, 30), ipadx=10, ipady=5)

    def login(self):
        email = self.email_entry.get()
        passwd = self.password_entry.get()

        response = requests.post("http://localhost:5000/auth/login", data={
            "email": email,
            "password": passwd
        })

        if response.status_code == 200:
            print(" Login successful!")
            user_data = response.json()
            print(" user_data received in GUI:", user_data)
            self.master.access_token = user_data["access_token"]
            self.master.user_id = user_data["user_id"]
            self.master.show_home(user_data=user_data)
        else:
            print(" Login failed:", response.text)
