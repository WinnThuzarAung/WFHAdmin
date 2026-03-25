import customtkinter as ctk
from datetime import datetime

class AttendanceFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, role):
        super().__init__(parent, fg_color="transparent")
        self.role = role
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header, text="Attendance Overview", font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")
        filter_frame = ctk.CTkFrame(header, fg_color="transparent")
        filter_frame.pack(side="right")
        month_var = ctk.StringVar(value=datetime.now().strftime("%B"))
        ctk.CTkOptionMenu(filter_frame, values=["January", "February", "March", "April", "May", "June",
                                                "July", "August", "September", "October", "November", "December"],
                          variable=month_var, width=120).pack(side="left", padx=5)
        year_var = ctk.StringVar(value=str(datetime.now().year))
        ctk.CTkOptionMenu(filter_frame, values=["2024", "2025", "2026"], variable=year_var, width=80).pack(side="left", padx=5)
        ctk.CTkButton(filter_frame, text="PDF Export", width=100).pack(side="left", padx=10)

        table_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_frame.pack(fill="x", padx=20, pady=10)
        headers = ["Emp ID", "Name", "Late Days", "Total Working Days", "Whole Leave", "Half Leave"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(table_frame, text=header, font=ctk.CTkFont(weight="bold"), width=120).grid(row=0, column=col, padx=2, pady=5)
        sample_data = [("E001", "John Doe", "2", "22", "1", "2"), ("E002", "Jane Smith", "0", "22", "0", "0"), ("E003", "Bob Johnson", "1", "20", "1", "1")]
        for row, data in enumerate(sample_data, start=1):
            for col, val in enumerate(data):
                ctk.CTkLabel(table_frame, text=val, width=120).grid(row=row, column=col, padx=2, pady=2)
