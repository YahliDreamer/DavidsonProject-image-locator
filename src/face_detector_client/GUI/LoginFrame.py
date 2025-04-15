import customtkinter as ctk
import requests


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
