import customtkinter as ctk
from tkinter import messagebox
from typing import Tuple, Optional
from dashboard import Dashboard

# Formal, modern theme setup
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

# Mock user data
MOCK_USERS = {
    "admin": {"password": "admin", "role": "admin"},
    "leader": {"password": "leader", "role": "leader"},
    "member": {"password": "member", "role": "member"},
}

def verify_user(username: str, password: str) -> Tuple[bool, Optional[str]]:
    user = MOCK_USERS.get(username)
    if user and user["password"] == password:
        return True, user["role"]
    return False, None


from dashboard import Dashboard

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MiniStore Enterprise Login")
        self.geometry("420x320")
        self.resizable(False, False)

        card = ctk.CTkFrame(self, corner_radius=15, border_width=2, border_color="#777")
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.89, relheight=0.85)

        header = ctk.CTkLabel(card, text="Welcome to MiniStore", font=ctk.CTkFont(size=20, weight="bold"))
        header.pack(pady=(15, 10))

        subtext = ctk.CTkLabel(card, text="Please sign in with your formal credentials", font=ctk.CTkFont(size=12))
        subtext.pack(pady=(0, 20))

        self.username_entry = ctk.CTkEntry(card, placeholder_text="Username", width=280)
        self.username_entry.pack(pady=(0, 12))

        self.password_entry = ctk.CTkEntry(card, placeholder_text="Password", show="*", width=280)
        self.password_entry.pack(pady=(0, 15))

        self.status_label = ctk.CTkLabel(card, text="", text_color="#ff5555")
        self.status_label.pack(pady=(0, 8))

        login_btn = ctk.CTkButton(card, text="Login", width=180, command=self.on_login)
        login_btn.pack(pady=(0, 10))

        provider = ctk.CTkLabel(card, text="Contact admin if you cannot login", font=ctk.CTkFont(size=10, slant="italic"))
        provider.pack(side="bottom", pady=10)

        self.bind('<Return>', lambda event=None: self.on_login())

    def on_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.status_label.configure(text="Username and password are required.")
            return

        self.status_label.configure(text="")

        success, role = verify_user(username, password)
        if success:
            # messagebox.showinfo(
            #     "Login Successful",
            #     f"Welcome, {username} ({role})!\nRedirecting to the dashboard..."
            # )
            # self.destroy()
            dashboard = Dashboard()
            dashboard.current_role = role
            dashboard.current_user = username
            # Show the correct page by role
            if role == "admin":
                dashboard.show_dashboard()
            elif role == "leader":
                dashboard.show_tasks()
            else:
                dashboard.show_activity()
            dashboard.mainloop()
        else:
            self.status_label.configure(text="Invalid username or password.")
            self.password_entry.delete(0, ctk.END)


if __name__ == '__main__':
    app = LoginWindow()
    app.mainloop()