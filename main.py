import customtkinter as ctk
from login import LoginWindow  # login.py ဖိုင်ထဲက LoginWindow ကို ခေါ်ယူခြင်း

def main():
    # Appearance Settings
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    # App Instance တည်ဆောက်ခြင်း
    app = LoginWindow()
    app.mainloop()

if __name__ == "__main__":
    main()