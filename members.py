import customtkinter as ctk

class MemberListFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header, text="Member List", font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")
        ctk.CTkButton(header, text="+ New Member", width=120).pack(side="right")
        for member in ["Alice Chen", "Bob Wang", "Carol Lee", "David Kim", "Ella Zhang"]:
            member_frame = ctk.CTkFrame(self, fg_color=("gray95", "gray20"), corner_radius=10)
            member_frame.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(member_frame, text=member, font=ctk.CTkFont(size=14)).pack(side="left", padx=15, pady=10)
            ctk.CTkButton(member_frame, text="Edit", width=60).pack(side="right", padx=10, pady=5)
            ctk.CTkButton(member_frame, text="Delete", width=60, fg_color="red", hover_color="darkred").pack(side="right", padx=5, pady=5)
