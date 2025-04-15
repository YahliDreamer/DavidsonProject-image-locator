import requests
import customtkinter as ctk
from tkinter import filedialog


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

