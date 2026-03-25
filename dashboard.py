
import customtkinter as ctk
from attendance import AttendanceFrame
from members import MemberListFrame
from daily_report import DailyReportFrame
from leave_request import LeaveRequestFrame
from placeholder import PlaceholderFrame
from tasks import TaskFrame
from activity import ActivityFrame

class Dashboard(ctk.CTk):
        def create_top_bar(self):
            ctk.CTkLabel(self.top_bar, text="⚡ WorkSync", font=ctk.CTkFont(size=20, weight="bold"),
                         text_color=("gray10", "gray90")).grid(row=0, column=0, padx=(20, 10), pady=20, sticky="w")
            ctk.CTkEntry(self.top_bar, placeholder_text="🔍 Search...", width=250, height=36,
                         corner_radius=18).grid(row=0, column=1, padx=15, pady=20, sticky="w")

            status_container = ctk.CTkFrame(self.top_bar, fg_color="transparent")
            status_container.grid(row=0, column=3, padx=10, pady=20)
            # If you have office_count_val and wfh_count_val, use them; else use static values
            office_count = getattr(self, 'office_count_val', 12)
            wfh_count = getattr(self, 'wfh_count_val', 8)
            self.office_count_label = ctk.CTkLabel(status_container, text=f"🏢 Office: {office_count}",
                                                   font=ctk.CTkFont(size=13, weight="bold"), text_color="#2ecc71")
            self.office_count_label.pack(side="left", padx=8)
            self.wfh_count_label = ctk.CTkLabel(status_container, text=f"🏠 WFH: {wfh_count}",
                                                font=ctk.CTkFont(size=13, weight="bold"), text_color="#3498db")
            self.wfh_count_label.pack(side="left", padx=8)

            profile_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
            profile_frame.grid(row=0, column=5, padx=(15, 25), pady=20)
            self.avatar = ctk.CTkFrame(profile_frame, width=38, height=38, corner_radius=19, fg_color=("#4a7c59", "#2c5a3e"))
            self.avatar.pack(side="left", padx=(0, 8))
            ctk.CTkLabel(self.avatar, text="JD", font=ctk.CTkFont(size=14, weight="bold"), text_color="white").place(relx=0.5, rely=0.5, anchor="center")
            ctk.CTkLabel(profile_frame, text="Jamie D. | member", font=ctk.CTkFont(size=13, weight="bold"), text_color="white").pack(side="left")
        def __init__(self):
            super().__init__()
            self.title("WorkSync – Role-Based UI")
            self.geometry("1200x750")
            self.minsize(1000, 600)

            # Grid config for main window
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)

            # Dashboard container (matches TeamsUI)
            self.dashboard_container = ctk.CTkFrame(self, fg_color="transparent")
            self.dashboard_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            self.dashboard_container.grid_rowconfigure(1, weight=1)
            self.dashboard_container.grid_columnconfigure(1, weight=1)

            # Top bar
            self.top_bar = ctk.CTkFrame(self.dashboard_container, height=70, corner_radius=0, fg_color=("#1f2937", "#1f2937"))
            self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
            self.top_bar.grid_columnconfigure(2, weight=1)
            self.top_bar.grid_columnconfigure(3, weight=0)
            self.top_bar.grid_columnconfigure(4, weight=0)
            self.create_top_bar()

            # Sidebar
            self.sidebar_frame = ctk.CTkFrame(self.dashboard_container, width=220, corner_radius=0, fg_color=("#253341", "#253341"))
            self.sidebar_frame.grid(row=1, column=0, sticky="nsew")
