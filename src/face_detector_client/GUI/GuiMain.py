import customtkinter as ctk

from src.face_detector_client.GUI.SignUpFrame import SignUpFrame
from src.face_detector_client.GUI.ReportFrame import ReportFrame
from src.face_detector_client.GUI.HomeFrame import HomeFrame
from src.face_detector_client.GUI.LoginFrame import LoginFrame


class GuiMain(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Face Recognition GUI")
        self.geometry("600x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

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
        self.reports_frame.set_user_data({
            "access_token": self.access_token,
            "user_id": self.user_id
        })
        self.reports_frame.pack(fill="both", expand=True)
        self.reports_frame.load_graphs()

    def show_home(self, user_data):
        self.login_frame.pack_forget()
        self.signup_frame.pack_forget()
        self.home_frame.set_user_data(user_data)

        self.home_frame.pack(fill="both", expand=True)
