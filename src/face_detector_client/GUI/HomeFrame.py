import webbrowser
import customtkinter as ctk
import requests


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

    def load_detections(self, filter_keyword=None):
        keyword = filter_keyword or self.search_var.get().lower().strip()

        # keyword = self.search_var.get().lower().strip()
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
