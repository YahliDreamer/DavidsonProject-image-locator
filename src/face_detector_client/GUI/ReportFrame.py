
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
import requests
import csv
from urllib.parse import urlparse


class ReportFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.chart_type = "Top Websites"
        self.graph_mode = "Bar"
        self.current_data = []

        self.label = ctk.CTkLabel(self, text="דוח הופעות לפי תמונה", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=10)

        self.graph_selector = ctk.CTkSegmentedButton(
            self, values=["Top Websites", "By Month"], command=self.render_selected_chart
        )
        self.graph_selector.pack(pady=5)

        self.mode_selector = ctk.CTkSegmentedButton(
            self, values=["Bar", "Line", "Dots"], command=self.set_graph_mode
        )
        self.mode_selector.pack(pady=5)

        self.load_button = ctk.CTkButton(self, text=" Load Report", command=self.load_graphs)
        self.load_button.pack(pady=5)

        self.export_csv = ctk.CTkButton(self, text="⬇ Export CSV", command=self.export_to_csv)
        self.export_csv.pack(pady=5)

        self.theme_switch = ctk.CTkSwitch(self, text=" Dark Mode", command=self.toggle_theme)
        self.theme_switch.pack(pady=5)

        self.chart_container = ctk.CTkFrame(self)
        self.chart_container.pack(expand=True, fill="both", padx=20, pady=10)

        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_container)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.access_token = None

    def toggle_theme(self):
        ctk.set_appearance_mode("dark" if self.theme_switch.get() else "light")

    def set_graph_mode(self, mode):
        self.graph_mode = mode
        self.load_graphs()

    def render_selected_chart(self, chart_type):
        self.chart_type = chart_type
        self.load_graphs()

    def load_graphs(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        labels = []
        values = []

        try:
            response = requests.get("http://localhost:5000/user/report", headers={"Authorization": f"Bearer {self.access_token}"})
            if response.status_code != 200:
                print(" Failed to fetch report:", response.text)
                return
            data = response.json()
        except Exception as e:
            print(" Error:", e)
            return

        if self.chart_type == "Top Websites":
            websites_data = data.get("top_websites", {})
            labels = list(websites_data.keys())
            values = list(websites_data.values())
            ax.set_title("Top Detected Websites")
            ax.set_xlabel("Website")

        elif self.chart_type == "By Month":
            labels = data.get("trend_months", [])
            values = data.get("trend_counts", [])
            ax.set_title("Detections Per Month")
            ax.set_xlabel("Month")

        if not labels:
            ax.text(0.5, 0.5, "No data available", ha='center', va='center', fontsize=12)
        else:
            if self.graph_mode == "Bar":
                ax.bar(labels, values, color="skyblue")
            elif self.graph_mode == "Line":
                ax.plot(labels, values, marker='o', linestyle='-', color="green")
            elif self.graph_mode == "Dots":
                ax.scatter(labels, values, color="lightgreen")

            ax.set_ylabel("Count")
            ax.tick_params(axis='x', labelrotation=45, labelsize=8)  #  smaller font
            self.figure.tight_layout()  #  auto adjust layout
        self.current_data = list(zip(labels, values))

        self.canvas.draw()

    def set_user_data(self, user_data):
        self.access_token = user_data.get("access_token")
        self.user_id = user_data.get("user_id")

    def export_to_csv(self):
        if not self.current_data:
            print(" No data to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path:
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Label", "Count"])
                writer.writerows(self.current_data)
            print(" Exported to", path)
