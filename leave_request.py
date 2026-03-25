import customtkinter as ctk

class LeaveRequestFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="Leave Request", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=20, pady=20)
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(form_frame, text="Leave Type:", font=ctk.CTkFont(size=14)).grid(row=0, column=0, sticky="w", pady=5)
        leave_type = ctk.CTkOptionMenu(form_frame, values=["Annual", "Sick", "Unpaid"], width=150)
        leave_type.grid(row=0, column=1, sticky="w", pady=5, padx=10)
        ctk.CTkLabel(form_frame, text="Start Date:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, sticky="w", pady=5)
        start_entry = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD", width=150)
        start_entry.grid(row=1, column=1, sticky="w", pady=5, padx=10)
        ctk.CTkLabel(form_frame, text="End Date:", font=ctk.CTkFont(size=14)).grid(row=2, column=0, sticky="w", pady=5)
        end_entry = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD", width=150)
        end_entry.grid(row=2, column=1, sticky="w", pady=5, padx=10)
        ctk.CTkLabel(form_frame, text="Reason:", font=ctk.CTkFont(size=14)).grid(row=3, column=0, sticky="w", pady=5)
        reason_text = ctk.CTkTextbox(form_frame, height=80, width=300)
        reason_text.grid(row=3, column=1, pady=5, padx=10)
        ctk.CTkButton(self, text="Submit Request", width=150).pack(pady=20)
