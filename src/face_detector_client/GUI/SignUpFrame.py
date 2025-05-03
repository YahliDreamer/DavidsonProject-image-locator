
import requests
import customtkinter as ctk
from tkinter import filedialog

class SignUpFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(fg_color="#ffe6f0")  # Light pink

        # 🔽 Scrollable container
        scroll_frame = ctk.CTkScrollableFrame(self, width=500, height=600)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 🌟 Title
        self.title_label = ctk.CTkLabel(
            scroll_frame,
            text="Create Your Account 🎀",
            font=("Comic Sans MS", 28, "bold"),
            text_color="#ff66b2"
        )
        self.title_label.pack(pady=(30, 20))

        # 📝 Name
        self.name_label = ctk.CTkLabel(scroll_frame, text="Name", font=("Comic Sans MS", 16, "bold"), text_color="#ff3399")
        self.name_label.pack(pady=(10, 5))
        self.name_entry = ctk.CTkEntry(scroll_frame, corner_radius=15, fg_color="#ffffff", text_color="#ff3399")
        self.name_entry.pack(pady=(0, 15), ipadx=10, ipady=5)

        # ✉️ Email
        self.email_label = ctk.CTkLabel(scroll_frame, text="Email", font=("Comic Sans MS", 16, "bold"), text_color="#ff3399")
        self.email_label.pack(pady=(10, 5))
        self.email_entry = ctk.CTkEntry(scroll_frame, corner_radius=15, fg_color="#ffffff", text_color="#ff3399")
        self.email_entry.pack(pady=(0, 15), ipadx=10, ipady=5)

        # 🔒 Password
        self.password_label = ctk.CTkLabel(scroll_frame, text="Password", font=("Comic Sans MS", 16, "bold"), text_color="#ff3399")
        self.password_label.pack(pady=(10, 5))
        self.password_entry = ctk.CTkEntry(scroll_frame, show="*", corner_radius=15, fg_color="#ffffff", text_color="#ff3399")
        self.password_entry.pack(pady=(0, 15), ipadx=10, ipady=5)

        # 📱 Phone
        self.phone_label = ctk.CTkLabel(scroll_frame, text="Phone", font=("Comic Sans MS", 16, "bold"), text_color="#ff3399")
        self.phone_label.pack(pady=(10, 5))
        self.phone_entry = ctk.CTkEntry(scroll_frame, corner_radius=15, fg_color="#ffffff", text_color="#ff3399")
        self.phone_entry.pack(pady=(0, 20), ipadx=10, ipady=5)

        # 🖼️ Upload Image Button
        self.image_path = ""
        self.upload_button = ctk.CTkButton(
            scroll_frame,
            text="📸 Upload Image",
            command=self.upload_image,
            fg_color="#ff66b2",
            hover_color="#ff99cc",
            corner_radius=20,
            font=("Comic Sans MS", 16, "bold")
        )
        self.upload_button.pack(pady=(5, 20), ipadx=10, ipady=5)

        # ✅ Submit Button
        self.submit_button = ctk.CTkButton(
            scroll_frame,
            text="✨ Submit ✨",
            command=self.signup,
            fg_color="#ff66b2",
            hover_color="#ff99cc",
            corner_radius=20,
            font=("Comic Sans MS", 16, "bold")
        )
        self.submit_button.pack(pady=(10, 10), ipadx=10, ipady=5)

        # 📩 Notification Checkboxes
        self.notify_email_check = ctk.CTkCheckBox(scroll_frame, text="📩 Email Notification")
        self.notify_email_check.pack(pady=(5, 5))
        self.notify_sms_check = ctk.CTkCheckBox(scroll_frame, text="📱 SMS Notification")
        self.notify_sms_check.pack(pady=(5, 15))

        # 🔙 Back Button (outside scroll frame)
        self.back_button = ctk.CTkButton(
            self,
            text="🔙 Back to Login",
            command=master.show_login,
            fg_color="#ffffff",
            text_color="#ff66b2",
            border_color="#ff66b2",
            border_width=2,
            hover_color="#ffe6f0",
            corner_radius=20,
            font=("Comic Sans MS", 16, "bold")
        )
        self.back_button.pack(pady=(0, 30), ipadx=10, ipady=5)

    def upload_image(self):
        path = filedialog.askopenfilename()
        self.image_path = path

    def signup(self):
        if not self.image_path:
            print("❌ Please upload an image.")
            return

        try:
            image_name = self.image_path.split("/")[-1]

            with open(self.image_path, "rb") as img_file:
                payload = {
                    "username": self.name_entry.get(),
                    "email": self.email_entry.get(),
                    "password": self.password_entry.get(),
                    "phone_number": self.phone_entry.get(),
                    "notify_email": str(self.notify_email_check.get()),  # "0" or "1"
                    "notify_sms": str(self.notify_sms_check.get()),  # "0" or "1"
                }
                files = {
                    "image": (image_name, img_file)
                }

                response = requests.post("http://localhost:5000/auth/register", data=payload, files=files)

            if response.status_code == 201:
                print("✅ Registered successfully!")
                self.master.show_login()
            else:
                print("❌ Registration failed:", response.text)

        except Exception as e:
            print(f"❌ Error during registration: {e}")
