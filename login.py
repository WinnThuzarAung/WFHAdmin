import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
from typing import Tuple, Optional

# Formal, modern theme setup
ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Options: "blue", "dark-blue", "green"


def verify_user(username: str, password: str) -> Tuple[bool, Optional[str]]:
    """Check credentials against the database."""
    try:
        db = mysql.connector.connect(
            user='root',
            password='root',
            host='127.0.0.1',
            database='ministore',
            auth_plugin='mysql_native_password'
        )
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT password, role FROM users WHERE user_name = %s",
            (username,)
        )
        row = cursor.fetchone()
        if row is None:
            return False, None

        # Basic plaintext comparison; update to hashing for production.
        if password == row['password']:
            return True, (row.get('role') or 'member').lower()
        return False, None

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Unable to verify user: {e}")
        return False, None

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db is not None and db.is_connected():
            db.close()


class LoginPage(ctk.CTk):
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
            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {username} ({role})!\nRedirecting to the dashboard..."
            )
            self.destroy()
        else:
            self.status_label.configure(text="Invalid username or password.")
            self.password_entry.delete(0, ctk.END)


if __name__ == '__main__':
    app = LoginPage()
    app.mainloop()