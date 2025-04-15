import requests
import customtkinter as ctk
from matplotlib.figure import Figure


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

