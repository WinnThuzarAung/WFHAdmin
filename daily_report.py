import customtkinter as ctk

class DailyReportFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="Daily Report", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=20, pady=20)
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(form_frame, text="Work Description:", font=ctk.CTkFont(size=14)).grid(row=0, column=0, sticky="w", pady=5)
        work_entry = ctk.CTkTextbox(form_frame, height=100, width=400)
        work_entry.grid(row=0, column=1, pady=5, padx=10)
        ctk.CTkLabel(form_frame, text="Hours Worked:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, sticky="w", pady=5)
        hours_entry = ctk.CTkEntry(form_frame, placeholder_text="e.g., 8", width=150)
        hours_entry.grid(row=1, column=1, sticky="w", pady=5, padx=10)
        ot_var = ctk.BooleanVar()
        ot_check = ctk.CTkCheckBox(form_frame, text="Overtime?", variable=ot_var)
        ot_check.grid(row=2, column=1, sticky="w", pady=5, padx=10)
        ctk.CTkButton(self, text="Submit Report", width=150).pack(pady=20)
