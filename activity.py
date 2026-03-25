import customtkinter as ctk
from data import activity_log

class ActivityFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, role, current_user):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="Activity Log", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=20, pady=20)
        for entry in activity_log:
            ctk.CTkLabel(self, text=entry, anchor="w").pack(fill="x", padx=20, pady=2)
