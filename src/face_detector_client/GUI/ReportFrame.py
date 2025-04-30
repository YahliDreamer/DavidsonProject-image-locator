import requests
import customtkinter as ctk
from matplotlib.figure import Figure
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
import csv
from tkinter import filedialog

# class ReportFrame(ctk.CTkFrame):
#     def __init__(self, master):
#         super().__init__(master)
#         self.master = master
#         self.graph_area = ctk.CTkFrame(self)
#         self.graph_area.pack(pady=10, fill="both", expand=True)
#
#         self.button_frame = ctk.CTkFrame(self)
#         self.button_frame.pack(pady=10)
#
#         # Graph control buttons
#         ctk.CTkButton(self.button_frame, text="Top Websites", command=self.plot_top_websites).grid(row=0, column=0, padx=10)
#         ctk.CTkButton(self.button_frame, text="Appearances by Year", command=self.plot_yearly_appearances).grid(row=0, column=1, padx=10)
#         ctk.CTkButton(self.button_frame, text="Top Platforms", command=self.plot_platform_distribution).grid(row=0, column=2, padx=10)
#         ctk.CTkButton(self.button_frame, text="Top Images", command=self.plot_top_images).grid(row=0, column=3, padx=10)
#
#         self.export_btn = ctk.CTkButton(self, text="Export Graph Data", command=self.export_csv)
#         self.export_btn.pack(pady=5)
#
#         self.theme_switch = ctk.CTkSwitch(self, text="Light/Dark Mode", command=self.toggle_theme)
#         self.theme_switch.pack()
#
#         # Color Palette
#         self.palette_frame = ctk.CTkFrame(self)
#         self.palette_frame.pack(pady=10)
#         for color in ["#1e1e1e", "#2e2e2e", "#3b3b3b", "#4b4b4b", "#5c5c5c"]:
#             ctk.CTkButton(self.palette_frame, width=20, height=20, fg_color=color, text="", command=lambda c=color: self.change_background(c)).pack(side="left", padx=5)
#
#         self.current_data = []  # Store current graph data
#
#     def toggle_theme(self):
#         current = ctk.get_appearance_mode()
#         new_mode = "light" if current == "dark" else "dark"
#         ctk.set_appearance_mode(new_mode)
#
#     def change_background(self, color):
#         self.configure(fg_color=color)
#         self.graph_area.configure(fg_color=color)
#
#     def export_csv(self):
#         if not self.current_data:
#             print("❌ No data to export.")
#             return
#         filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
#         if filepath:
#             with open(filepath, mode='w', newline='') as file:
#                 writer = csv.writer(file)
#                 writer.writerows(self.current_data)
#             print(f"✅ Data exported to {filepath}")
#
#     def fetch_data(self, graph_type):
#         try:
#             response = requests.get(f"http://localhost:5000/user/report?graph={graph_type}")
#             if response.status_code == 200:
#                 return response.json()
#             else:
#                 print("❌ Failed to fetch data:", response.text)
#         except Exception as e:
#             print("❌ Error fetching data:", e)
#         return []
#
#     def plot_graph(self, title, labels, values):
#         for widget in self.graph_area.winfo_children():
#             widget.destroy()
#
#         fig, ax = plt.subplots(figsize=(6, 4))
#         ax.bar(labels, values, edgecolor="black")
#         ax.set_title(title)
#         ax.set_ylabel("Count")
#         ax.set_xticklabels(labels, rotation=45, ha='right')
#
#         canvas = FigureCanvasTkAgg(fig, master=self.graph_area)
#         canvas.draw()
#         canvas.get_tk_widget().pack(fill="both", expand=True)
#
#         # Save current data for export
#         self.current_data = [("Label", "Value")] + list(zip(labels, values))
#
#     def plot_top_websites(self):
#         data = self.fetch_data("top_websites")
#         labels = [entry["domain"] for entry in data]
#         values = [entry["count"] for entry in data]
#         self.plot_graph("Top Websites", labels, values)
#
#     def plot_yearly_appearances(self):
#         data = self.fetch_data("by_year")
#         labels = [entry["year"] for entry in data]
#         values = [entry["count"] for entry in data]
#         self.plot_graph("Appearances Over 10 Years", labels, values)
#
#     def plot_platform_distribution(self):
#         data = self.fetch_data("platforms")
#         labels = [entry["platform"] for entry in data]
#         values = [entry["count"] for entry in data]
#         self.plot_graph("Platform Distribution", labels, values)
#
#     def plot_top_images(self):
#         data = self.fetch_data("top_images")
#         labels = [f"Img {i+1}" for i in range(len(data))]
#         values = [entry["count"] for entry in data]
#         self.plot_graph("Top Images Online", labels, values)
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
from tkinter import filedialog

class ReportFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = ctk.CTkLabel(self, text="📈 Advanced Report Dashboard", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=10)

        # Theme and layout controls
        self.theme_switch = ctk.CTkSwitch(self, text="🌙 Dark Mode", command=self.toggle_theme)
        self.theme_switch.pack(pady=10)

        self.graph_selector = ctk.CTkSegmentedButton(self, values=["Bar", "Line", "Pie"],
                                                     command=self.render_selected_chart)
        self.graph_selector.pack(pady=5)

        self.year_filter = ctk.CTkComboBox(self, values=["All", "2023", "2024", "2025"], command=self.apply_filter)
        self.year_filter.set("All")
        self.year_filter.pack(pady=5)

        self.load_button = ctk.CTkButton(self, text="📊 Load another Report", command=self.load_graphs)
        self.load_button.pack(pady=5)

        self.export_csv = ctk.CTkButton(self, text="⬇ Export CSV", command=self.export_to_csv)
        self.export_csv.pack(pady=5)

        self.export_pdf = ctk.CTkButton(self, text="🧾 Export PDF", command=self.export_to_pdf)
        self.export_pdf.pack(pady=5)

        # Container for charts
        self.chart_container = ctk.CTkFrame(self)
        self.chart_container.pack(expand=True, fill="both", padx=20, pady=10)

        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_container)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def toggle_theme(self):
        mode = "dark" if self.theme_switch.get() else "light"
        ctk.set_appearance_mode(mode)

    def render_selected_chart(self, chart_type):
        # Will dynamically choose which chart to render
        self.load_graphs(chart_type)

    def apply_filter(self, selected_year):
        print(f"📆 Filter set to year: {selected_year}")
        self.load_graphs()

    def load_graphs(self, chart_type="Bar"):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Sample data (to be replaced with API-driven stats)
        categories = ["Facebook", "Instagram", "Reddit", "YouTube"]
        values = [12, 7, 4, 9]

        if chart_type == "Bar":
            ax.bar(categories, values)
        elif chart_type == "Line":
            ax.plot(categories, values, marker='o')
        elif chart_type == "Pie":
            ax.pie(values, labels=categories, autopct='%1.1f%%')

        ax.set_title(f"Detections by Platform ({chart_type})")
        self.canvas.draw()

    def export_to_csv(self):
        # Placeholder
        filedialog.asksaveasfilename(defaultextension=".csv")
        print("✅ CSV Exported")

    def export_to_pdf(self):
        # Placeholder
        filedialog.asksaveasfilename(defaultextension=".pdf")
        print("✅ PDF Exported")
