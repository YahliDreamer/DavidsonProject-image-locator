from time import sleep

import customtkinter as ctk
from PIL import Image, ImageDraw
import requests
import io
import os
import webbrowser
import random

class HomeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Initial futuristic theme
        self.primary_color = "#00f0ff"  # Neon cyan
        self.background_color = "#0d0d0d"  # Deep black
        self.secondary_color = "#1a1a1a"  # Darker gray
        self.font_family = "Segoe UI"  # Modern font

        self.configure(fg_color=self.background_color)

        self.profile_img = None
        self.access_token = None
        self.detections = []
        self.detections_timeout = 30

        # 🚀 Title
        self.title_label = ctk.CTkLabel(
            self,
            text="HOME",
            font=(self.font_family, 28, "bold"),
            text_color=self.primary_color
        )
        self.title_label.pack(pady=(20, 10))

        # 🚀 Profile Card
        self.profile_frame = ctk.CTkFrame(self, corner_radius=15, fg_color=self.secondary_color)
        self.profile_frame.pack(pady=10, padx=20, fill="x")

        self.profile_pic_label = ctk.CTkLabel(self.profile_frame, text="")
        self.profile_pic_label.pack(side="left", padx=15, pady=10)

        self.profile_text = ctk.CTkLabel(
            self.profile_frame,
            text="Hello User!",
            font=(self.font_family, 18, "bold"),
            text_color=self.primary_color
        )
        self.profile_text.pack(side="left", padx=10)

        # 🚀 View Reports Button
        self.report_button = ctk.CTkButton(
            self,
            text="📊 View Reports",
            height=45,
            corner_radius=10,
            font=(self.font_family, 16, "bold"),
            fg_color=self.primary_color,
            text_color="#0d0d0d",
            hover_color="#00cccc",
            command=master.show_report
        )
        self.report_button.pack(pady=(10, 10))

        # 🚀 Change Theme Button
        self.color_button = ctk.CTkButton(
            self,
            text="🎨 Switch Theme",
            height=40,
            corner_radius=10,
            font=(self.font_family, 14, "bold"),
            fg_color=self.primary_color,
            text_color="#0d0d0d",
            hover_color="#00cccc",
            command=self.change_theme
        )
        self.color_button.pack(pady=(0, 20))

        # 🚀 Scrollable detection container
        self.scrollable_container = ctk.CTkScrollableFrame(
            self, width=600, height=500, fg_color=self.secondary_color
        )
        self.scrollable_container.pack(padx=20, pady=10, fill="both", expand=True)

    def set_user_data(self, user_data):
        self.access_token = user_data.get('access_token', '')
        username = user_data.get('username', 'User')
        self.profile_text.configure(text=f"Welcome {username}!")

        image_url = user_data.get('image_url')
        if image_url:
            try:
                if image_url.startswith('http'):
                    response = requests.get(image_url)
                    response.raise_for_status()
                    image_data = Image.open(io.BytesIO(response.content))
                else:
                    if not os.path.exists(image_url):
                        image_url = os.path.join('src', 'face_detector_server', image_url)
                    image_data = Image.open(image_url)

                image_data = self.crop_to_circle(image_data)
                self.profile_img = ctk.CTkImage(image_data, size=(80, 80))
                self.profile_pic_label.configure(image=self.profile_img, text="")
            except Exception as e:
                print("❌ Error loading profile image:", e)

        self.after(100, self.load_detections)

    def crop_to_circle(self, img):
        size = (min(img.size),) * 2
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        output = Image.new('RGBA', size)
        output.paste(img.resize(size), (0, 0), mask)
        return output

    def change_theme(self):
        """Switch to a new futuristic random theme."""
        themes = [
            {"primary": "#00f0ff", "background": "#0d0d0d", "secondary": "#1a1a1a"},  # Cyan / black
            {"primary": "#ff00ff", "background": "#0a0a23", "secondary": "#1a1a40"},  # Purple neon
            {"primary": "#00ff88", "background": "#0b1a1a", "secondary": "#1a3333"},  # Green neon
            {"primary": "#ff6600", "background": "#1a0b00", "secondary": "#331a00"},  # Orange futuristic
        ]
        new_theme = random.choice(themes)

        self.primary_color = new_theme["primary"]
        self.background_color = new_theme["background"]
        self.secondary_color = new_theme["secondary"]

        self.apply_theme()

    def apply_theme(self):
        """Apply the selected theme to all widgets."""
        self.configure(fg_color=self.background_color)
        self.scrollable_container.configure(fg_color=self.secondary_color)
        self.profile_frame.configure(fg_color=self.secondary_color)

        self.title_label.configure(text_color=self.primary_color)
        self.profile_text.configure(text_color=self.primary_color)
        self.report_button.configure(fg_color=self.primary_color, hover_color=self.secondary_color, text_color=self.background_color)
        self.color_button.configure(fg_color=self.primary_color, hover_color=self.secondary_color, text_color=self.background_color)

        for widget in self.scrollable_container.winfo_children():
            widget.configure(fg_color=self.secondary_color)

    def load_detections(self):
        elapsed_time = 0
        sleep_interval = 5
        ctk.CTkLabel(
            self.scrollable_container,
            text="Waiting for detections...",
            font=(self.font_family, 16),
            text_color=self.primary_color
        ).pack(pady=10)
        try:
            while not self.detections and elapsed_time < self.detections_timeout:
                sleep(sleep_interval)  # wait between each iteration
                elapsed_time += sleep_interval

                response = requests.get(
                    "http://localhost:5000/user/detections?limit=50",
                    headers={"Authorization": f"Bearer {self.access_token}"}
                    )
                if response.status_code != 200:
                    print("❌ Failed to load detections:", response.text)
                    continue

                self.detections = response.json()

                self.detections = sorted(
                    self.detections, key=lambda x: x.get('timestamp', '')
                )
                if self.detections:
                    for widget in self.scrollable_container.winfo_children():
                        widget.destroy()

                    self.show_detections_animated(0)
                    return

                message = f"❌ Failed to load detections after timeout of {self.detections_timeout} seconds"
        except Exception as e:
            message = f"❌ Error loading detections:{e}"
            print(message)

        ctk.CTkLabel(
            self.scrollable_container,
            text=message,
            font=(self.font_family, 16),
            text_color=self.primary_color
        ).pack(pady=10)

    def show_detections_animated(self, index):
        if index >= len(self.detections):
            return

        det = self.detections[index]
        website = det["website_url"]
        timestamp = det.get("timestamp", "Unknown")

        # Detection Card
        bubble = ctk.CTkFrame(self.scrollable_container, fg_color=self.secondary_color, corner_radius=15)
        bubble.pack(anchor="w", padx=20, pady=10, ipadx=10, ipady=5)

        link_btn = ctk.CTkButton(
            bubble,
            text=website,
            text_color=self.primary_color,
            font=(self.font_family, 14),
            fg_color="transparent",
            hover_color=self.background_color,
            anchor="w",
            command=lambda url=website: webbrowser.open(url)
        )
        link_btn.pack(side="top", anchor="w", padx=5, pady=2)

        time_label = ctk.CTkLabel(
            bubble,
            text=f"🕓 {timestamp}",
            font=(self.font_family, 10),
            text_color="#999999"
        )
        time_label.pack(side="top", anchor="w", padx=5, pady=2)

        self.after(150, lambda: self.show_detections_animated(index + 1))
