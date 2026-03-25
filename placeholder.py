import customtkinter as ctk

class PlaceholderFrame(ctk.CTkFrame):
    def __init__(self, parent, title):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=24, weight="bold")).pack(pady=50)
