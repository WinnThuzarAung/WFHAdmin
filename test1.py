import customtkinter as ctk
from datetime import datetime, timedelta
from tkinter import messagebox
from login import verify_user


# ---------- Appearance Settings ----------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Global mock data
tasks = [
    {
        "id": 1,
        "title": "Prepare Q1 report",
        "description": "Collect data from all departments",
        "start_date": "2025-03-25",
        "duration": 3,
        "end_date": "2025-03-27",
        "assigned_to": "Jamie D.",
        "created_by": "Admin"
    },
    {
        "id": 2,
        "title": "Design review",
        "description": "Review new UI mockups",
        "start_date": "2025-03-26",
        "duration": 1,
        "end_date": "2025-03-26",
        "assigned_to": "Alex K.",
        "created_by": "Leader"
    },
    {
        "id": 3,
        "title": "Update documentation",
        "description": "Add new features to docs",
        "start_date": "2025-03-28",
        "duration": 2,
        "end_date": "2025-03-29",
        "assigned_to": "Jamie D.",
        "created_by": "Leader"
    }
]
next_task_id = 4

# Static member list for assignee dropdown
members = ["Jamie D.", "Alice Chen", "Bob Wang", "Carol Lee"]

# Activity log (for Admin)
activity_log = []


def add_activity(message):
    activity_log.insert(0, f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - {message}")


# ------------------------------------------------------------------
# Placeholder frames for other pages
# ------------------------------------------------------------------
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


class DailyReportFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="Daily Report", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=20, pady=20)
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(form_frame, text="Work Description:", font=ctk.CTkFont(size=14)).grid(row=0, column=0, sticky="w", pady=5)
        work_entry = ctk.CTkTextbox(form_frame, height=100, width=400)
        work_entry.grid(row=0, column=1, pady=5, padx=10)

        # Hours Worked and Overtime checkbox
        ctk.CTkLabel(form_frame, text="Hours Worked:", font=ctk.CTkFont(size=14)).grid(row=1, column=0, sticky="w", pady=5)
        hours_entry = ctk.CTkEntry(form_frame, placeholder_text="e.g., 8", width=150)
        hours_entry.grid(row=1, column=1, sticky="w", pady=5, padx=10)

        ot_var = ctk.BooleanVar()
        ot_check = ctk.CTkCheckBox(form_frame, text="Overtime?", variable=ot_var)
        ot_check.grid(row=2, column=1, sticky="w", pady=5, padx=10)

        ctk.CTkButton(self, text="Submit Report", width=150).pack(pady=20)


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


class PlaceholderFrame(ctk.CTkFrame):
    def __init__(self, parent, title):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=24, weight="bold")).pack(pady=50)


# ------------------------------------------------------------------
# New Frames: TaskFrame and ActivityFrame
# ------------------------------------------------------------------
class TaskFrame(ctk.CTkScrollableFrame):
    """Task list with creation capability. Mode: 'member' or 'leader'."""
    def __init__(self, parent, mode, current_user="Jamie D."):
        super().__init__(parent, fg_color="transparent")
        self.mode = mode
        self.current_user = current_user

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header, text="Tasks", font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")
        ctk.CTkButton(header, text="+ New Task", command=self.show_create_dialog).pack(side="right")

        # Task list container
        self.tasks_container = ctk.CTkFrame(self, fg_color="transparent")
        self.tasks_container.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh_task_list()

    def refresh_task_list(self):
        # Clear existing widgets
        for widget in self.tasks_container.winfo_children():
            widget.destroy()

        # Filter tasks based on mode
        if self.mode == "member":
            filtered = [t for t in tasks if t["assigned_to"] == self.current_user]
        else:  # leader: show all tasks
            filtered = tasks

        if not filtered:
            ctk.CTkLabel(self.tasks_container, text="No tasks found.").pack(pady=20)
            return

        for task in filtered:
            task_card = ctk.CTkFrame(self.tasks_container, corner_radius=12, fg_color=("gray94", "gray20"))
            task_card.pack(fill="x", pady=8, padx=5)
            task_card.grid_columnconfigure(1, weight=1)

            # Title and assignee (if leader)
            title_label = ctk.CTkLabel(task_card, text=task["title"], font=ctk.CTkFont(size=15, weight="bold"))
            title_label.grid(row=0, column=0, padx=15, pady=(10, 0), sticky="w")
            if self.mode == "leader":
                assignee_label = ctk.CTkLabel(task_card, text=f"Assigned to: {task['assigned_to']}", font=ctk.CTkFont(size=12), text_color="gray")
                assignee_label.grid(row=0, column=1, padx=15, pady=(10, 0), sticky="e")

            # Description
            desc_label = ctk.CTkLabel(task_card, text=task["description"], font=ctk.CTkFont(size=12), wraplength=400, justify="left")
            desc_label.grid(row=1, column=0, columnspan=2, padx=15, pady=(5, 0), sticky="w")

            # Dates
            dates = f"Start: {task['start_date']} | Duration: {task['duration']} day(s) | End: {task['end_date']}"
            date_label = ctk.CTkLabel(task_card, text=dates, font=ctk.CTkFont(size=11), text_color="gray")
            date_label.grid(row=2, column=0, columnspan=2, padx=15, pady=(0, 10), sticky="w")

    def show_create_dialog(self):
        # Create a popup window for task creation
        dialog = ctk.CTkToplevel(self)
        dialog.title("Create New Task")
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)

        # Form fields
        ctk.CTkLabel(dialog, text="Title:", font=ctk.CTkFont(size=14)).pack(pady=(10, 0))
        title_entry = ctk.CTkEntry(dialog, width=300)
        title_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Description:", font=ctk.CTkFont(size=14)).pack(pady=(10, 0))
        desc_text = ctk.CTkTextbox(dialog, height=100, width=300)
        desc_text.pack(pady=5)

        ctk.CTkLabel(dialog, text="Start Date (YYYY-MM-DD):", font=ctk.CTkFont(size=14)).pack(pady=(10, 0))
        start_entry = ctk.CTkEntry(dialog, width=200)
        start_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Duration (days):", font=ctk.CTkFont(size=14)).pack(pady=(10, 0))
        duration_entry = ctk.CTkEntry(dialog, width=100)
        duration_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="End Date (YYYY-MM-DD):", font=ctk.CTkFont(size=14)).pack(pady=(10, 0))
        end_entry = ctk.CTkEntry(dialog, width=200)
        end_entry.pack(pady=5)

        # For leader mode: assignee dropdown
        assignee_var = ctk.StringVar()
        if self.mode == "leader":
            ctk.CTkLabel(dialog, text="Assign to:", font=ctk.CTkFont(size=14)).pack(pady=(10, 0))
            assignee_menu = ctk.CTkOptionMenu(dialog, values=members, variable=assignee_var)
            assignee_menu.pack(pady=5)

        def create_task():
            title = title_entry.get().strip()
            description = desc_text.get("1.0", "end-1c").strip()
            start = start_entry.get().strip()
            duration = duration_entry.get().strip()
            end = end_entry.get().strip()
            if not title or not start or not duration or not end:
                messagebox.showerror("Error", "Please fill all required fields.")
                return
            try:
                duration = int(duration)
            except:
                messagebox.showerror("Error", "Duration must be a number.")
                return

            assignee = assignee_var.get() if self.mode == "leader" else self.current_user
            if not assignee:
                assignee = self.current_user  # fallback

            global next_task_id
            new_task = {
                "id": next_task_id,
                "title": title,
                "description": description,
                "start_date": start,
                "duration": duration,
                "end_date": end,
                "assigned_to": assignee,
                "created_by": self.current_user
            }
            tasks.append(new_task)
            next_task_id += 1

            # Add activity log for admin (if admin role exists)
            add_activity(f"New task '{title}' created by {self.current_user} for {assignee}")

            dialog.destroy()
            self.refresh_task_list()
            messagebox.showinfo("Success", "Task created successfully!")

        ctk.CTkButton(dialog, text="Create", command=create_task).pack(pady=20)


class ActivityFrame(ctk.CTkScrollableFrame):
    """Notification panel."""
    def __init__(self, parent, role, current_user="Jamie D."):
        super().__init__(parent, fg_color="transparent")
        self.role = role
        self.current_user = current_user

        ctk.CTkLabel(self, text="Activity Feed", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=20, pady=20)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh_activity()

    def refresh_activity(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        # Generate notifications
        notifications = []

        # Task deadline notifications (for all roles, but content may differ)
        today = datetime.now().date()
        for task in tasks:
            try:
                end_date = datetime.strptime(task["end_date"], "%Y-%m-%d").date()
                days_left = (end_date - today).days
                if 0 <= days_left <= 3:  # deadline approaching
                    if self.role == "member" and task["assigned_to"] == self.current_user:
                        notifications.append(f"Task '{task['title']}' is due in {days_left} day(s).")
                    elif self.role == "leader" and task["assigned_to"] != self.current_user:
                        notifications.append(f"Task '{task['title']}' assigned to {task['assigned_to']} is due in {days_left} day(s).")
                    elif self.role == "admin":
                        notifications.append(f"Task '{task['title']}' assigned to {task['assigned_to']} is due in {days_left} day(s).")
            except:
                pass

        # For admin: also show task creation logs
        if self.role == "admin":
            notifications.extend(activity_log[:10])  # show recent 10

        if not notifications:
            ctk.CTkLabel(self.container, text="No new notifications.").pack(pady=20)
        else:
            for note in notifications:
                card = ctk.CTkFrame(self.container, corner_radius=12, fg_color=("gray94", "gray20"))
                card.pack(fill="x", pady=5, padx=5)
                ctk.CTkLabel(card, text=note, font=ctk.CTkFont(size=13), wraplength=500, justify="left").pack(padx=15, pady=10)


# ------------------------------------------------------------------
# Main Application (same structure, updated sidebar)
# ------------------------------------------------------------------
class TeamsUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WorkSync – Role-Based UI")
        self.geometry("1200x750")
        self.minsize(1000, 600)

        self.current_role = "Member"
        self.current_user = None
        self.current_page = None
        self.office_count_val = 12
        self.wfh_count_val = 8
        self.user_status = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Login frame
        self.login_frame = ctk.CTkFrame(self, corner_radius=20)
        self.login_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.create_login_ui()

        # Dashboard container
        self.dashboard_container = ctk.CTkFrame(self, fg_color="transparent")
        self.dashboard_container.grid_rowconfigure(1, weight=1)
        self.dashboard_container.grid_columnconfigure(1, weight=1)

        self.top_bar = ctk.CTkFrame(self.dashboard_container, height=70, corner_radius=0, fg_color=("#1f2937", "#1f2937"))
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.top_bar.grid_columnconfigure(2, weight=1)
        self.top_bar.grid_columnconfigure(3, weight=0)
        self.top_bar.grid_columnconfigure(4, weight=0)
        self.create_top_bar()

        self.sidebar_frame = None
        self.content_frame = ctk.CTkFrame(self.dashboard_container, fg_color="transparent")
        self.content_frame.grid(row=1, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.dashboard_container.grid_forget()
        self.login_frame.grid(row=0, column=0, sticky="nsew")

    def create_login_ui(self):
        self.login_frame.grid_rowconfigure(0, weight=1)
        self.login_frame.grid_rowconfigure(4, weight=1)
        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_columnconfigure(2, weight=1)

        self.login_card = ctk.CTkFrame(self.login_frame, width=400, height=500, corner_radius=20)
        self.login_card.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        self.login_card.grid_propagate(False)

        ctk.CTkLabel(self.login_card, text="⚡ WorkSync", font=ctk.CTkFont(size=32, weight="bold"),
                     text_color=("#2ecc71", "#2ecc71")).pack(pady=(40, 20))
        ctk.CTkLabel(self.login_card, text="Sign in to continue", font=ctk.CTkFont(size=14),
                     text_color=("gray50", "gray60")).pack(pady=(0, 20))

        self.username_entry = ctk.CTkEntry(self.login_card, placeholder_text="Email", width=280, height=45, corner_radius=12)
        self.username_entry.pack(pady=10, padx=20)
        self.password_entry = ctk.CTkEntry(self.login_card, placeholder_text="Password", width=280, height=45,
                                           corner_radius=12, show="•")
        self.password_entry.pack(pady=10, padx=20)

        self.login_button = ctk.CTkButton(self.login_card, text="Login", width=280, height=45, corner_radius=12,
                                          font=ctk.CTkFont(size=14, weight="bold"), command=self.on_login)
        self.login_button.pack(pady=20, padx=20)

        ctk.CTkLabel(self.login_card, text="(Just click Login – no credentials needed)", font=ctk.CTkFont(size=11),
                     text_color=("gray50", "gray60")).pack(pady=(10, 0))

    def on_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # If no credentials provided, use defaults
        if not username:
            username = "admin"
        if not password:
            password = "admin"

        logged_in, db_role = verify_user(username, password)
        if not logged_in:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            self.password_entry.delete(0, "end")
            return

        self.current_user = username
        self.user_role = db_role.lower() if isinstance(db_role, str) and db_role.strip() else "member"
        self.current_role = self.user_role
        if self.current_role not in ("admin", "leader", "member"):
            self.current_role = "member"

        # Set status based on role
        if self.current_role == "admin":
            self.on_status_change("🏢 Office")
        elif self.current_role == "leader":
            self.on_status_change("🏢 Office")
        else:
            self.on_status_change("🏠 WFH")

        self.user_label.configure(text=f"{username[:12]} | {self.current_role}")
        self.avatar_label.configure(text=username[0].upper())

        # Do not reset dashboard counters here; this clears role-based status change
        self.build_sidebar()
        self.login_frame.grid_forget()
        self.dashboard_container.grid(row=0, column=0, sticky="nsew")
        self.show_default_page()

    def create_top_bar(self):
        ctk.CTkLabel(self.top_bar, text="⚡ WorkSync", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=("gray10", "gray90")).grid(row=0, column=0, padx=(20, 10), pady=20, sticky="w")
        ctk.CTkEntry(self.top_bar, placeholder_text="🔍 Search...", width=250, height=36,
                     corner_radius=18).grid(row=0, column=1, padx=15, pady=20, sticky="w")

        status_container = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        status_container.grid(row=0, column=3, padx=10, pady=20)
        self.office_count_label = ctk.CTkLabel(status_container, text=f"🏢 Office: {self.office_count_val}",
                                               font=ctk.CTkFont(size=13, weight="bold"), text_color="#2ecc71")
        self.office_count_label.pack(side="left", padx=8)
        self.wfh_count_label = ctk.CTkLabel(status_container, text=f"🏠 WFH: {self.wfh_count_val}",
                                            font=ctk.CTkFont(size=13, weight="bold"), text_color="#3498db")
        self.wfh_count_label.pack(side="left", padx=8)

        profile_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        profile_frame.grid(row=0, column=5, padx=(15, 25), pady=20)
        self.avatar = ctk.CTkFrame(profile_frame, width=38, height=38, corner_radius=19, fg_color=("#4a7c59", "#2c5a3e"))
        self.avatar.pack(side="left", padx=(0, 8))
        self.avatar_label = ctk.CTkLabel(self.avatar, text="JD", font=ctk.CTkFont(size=14, weight="bold"), text_color="white")
        self.avatar_label.place(relx=0.5, rely=0.5, anchor="center")
        self.user_label = ctk.CTkLabel(profile_frame, text="Jamie D. | member", font=ctk.CTkFont(size=13, weight="bold"), text_color="white")
        self.user_label.pack(side="left")

    # no on_role_change needed because role comes from login DB and is not editable in UI
    def on_role_change(self, new_role):
        pass

    def build_sidebar(self):
        if self.sidebar_frame:
            self.sidebar_frame.destroy()
        self.sidebar_frame = ctk.CTkFrame(self.dashboard_container, width=220, corner_radius=0,
                                          fg_color=("#253341", "#253341"))
        self.sidebar_frame.grid(row=1, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)

        self.sidebar_frame.grid_rowconfigure(0, weight=0)
        for i in range(1, 10):
            self.sidebar_frame.grid_rowconfigure(i, weight=0)
        self.sidebar_frame.grid_rowconfigure(99, weight=1)
        self.sidebar_frame.grid_rowconfigure(100, weight=0)
        self.sidebar_frame.grid_rowconfigure(101, weight=0)

        ctk.CTkLabel(self.sidebar_frame, text="MENU", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=("#e5e7eb", "#e5e7eb")).grid(row=0, column=0, padx=20, pady=(25, 15), sticky="w")

        row = 1
        if self.current_role == "admin":
            buttons = [
                ("📊  Dashboard", self.show_dashboard),
                ("📰  Activity", self.show_activity),
                ("👥  Member List", self.show_member_list),
                ("📅  Attendance", self.show_attendance),
            ]
        elif self.current_role == "leader":
            buttons = [
                ("📊  Dashboard", self.show_dashboard),
                ("📰  Activity", self.show_activity),
                ("✅  Tasks", self.show_tasks_leader),
                ("📁  Project", self.show_placeholder, "Project Management"),
                ("🏠  WFH Schedule", self.show_placeholder, "WFH Schedule"),
                ("📅  Attendance", self.show_attendance),
            ]
        else:  # member
            buttons = [
                ("📊  Dashboard", self.show_dashboard),
                ("📰  Activity", self.show_activity),
                ("✅  Tasks", self.show_tasks_member),
                ("📈  Daily Report", self.show_daily_report),
                ("🏖️  Leave Request", self.show_leave_request),
            ]

        for text, command, *args in buttons:
            btn = ctk.CTkButton(self.sidebar_frame, text=text, anchor="w", font=ctk.CTkFont(size=14),
                                height=44, corner_radius=12,
                                fg_color=("#2b3d50", "#1f2d3f"),
                                text_color=("#f8fafc", "#f8fafc"),
                                hover_color=("#374962", "#334155"))
            if args:
                btn.configure(command=lambda cmd=command, arg=args[0]: cmd(arg))
            else:
                btn.configure(command=command)
            btn.grid(row=row, column=0, padx=15, pady=6, sticky="ew")
            row += 1

        # Status selector
        status_section = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        status_section.grid(row=100, column=0, padx=15, pady=(0, 10), sticky="ew")
        ctk.CTkLabel(status_section, text="Your Status", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=("gray40", "gray60")).pack(anchor="w", pady=(0, 8))
        self.status_selector = ctk.CTkSegmentedButton(status_section, values=["🏢 Office", "🏠 WFH"],
                                                      command=self.on_status_change,
                                                      font=ctk.CTkFont(size=13, weight="bold"),
                                                      selected_color=("#2ecc71", "#2c7a4d"),
                                                      unselected_color=("gray80", "gray25"),
                                                      selected_hover_color=("#27ae60", "#1f6e43"),
                                                      corner_radius=18, height=36)
        self.status_selector.pack(fill="x")

        ctk.CTkButton(self.sidebar_frame, text="🚪  Logout", anchor="w", font=ctk.CTkFont(size=14, weight="bold"),
                      height=44, corner_radius=12,
                      fg_color=("#2b3d50", "#2b3d50"), hover_color=("#374962", "#374962"),
                      text_color=("#ffffff", "#ffffff"),                     
                      command=self.on_logout).grid(row=101, column=0, padx=15, pady=(8, 20), sticky="ew")

    def show_frame(self, frame_class, *args):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.current_page = frame_class(self.content_frame, *args) if args else frame_class(self.content_frame)
        self.current_page.pack(fill="both", expand=True)

    def show_default_page(self):
        if self.current_role == "admin":
            self.show_dashboard()
        else:
            self.show_dashboard()

    def show_dashboard(self):
        self.show_frame(PlaceholderFrame, "Dashboard – Coming Soon")

    def show_activity(self):
        current_user = self.current_user or "Jamie D."
        self.show_frame(ActivityFrame, self.current_role, current_user)

    def show_member_list(self):
        self.show_frame(MemberListFrame)

    def show_attendance(self):
        self.show_frame(AttendanceFrame, self.current_role)

    def show_daily_report(self):
        self.show_frame(DailyReportFrame)

    def show_leave_request(self):
        self.show_frame(LeaveRequestFrame)

    def show_tasks_member(self):
        current_user = self.current_user or "Jamie D."
        self.show_frame(TaskFrame, "member", current_user)

    def show_tasks_leader(self):
        current_user = self.current_user or "Jamie D."
        self.show_frame(TaskFrame, "leader", current_user)

    def show_placeholder(self, title):
        self.show_frame(PlaceholderFrame, title)

    def on_status_change(self, selected_value):
        if not selected_value:
            return
        new_status = "office" if selected_value == "🏢 Office" else "wfh"
        if self.user_status == new_status:
            return
        if self.user_status == "office":
            self.office_count_val -= 1
        elif self.user_status == "wfh":
            self.wfh_count_val -= 1
        if new_status == "office":
            self.office_count_val += 1
        else:
            self.wfh_count_val += 1
        self.user_status = new_status
        self.office_count_label.configure(text=f"🏢 Office: {self.office_count_val}")
        self.wfh_count_label.configure(text=f"🏠 WFH: {self.wfh_count_val}")

    def on_logout(self):
        self.dashboard_container.grid_forget()
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.user_label.configure(text="Jamie D. | member")
        self.avatar_label.configure(text="JD")
        self.current_role = "member"
        self.current_user = None
        self.reset_dashboard_state()

    def reset_dashboard_state(self):
        self.office_count_val = 12
        self.wfh_count_val = 8
        self.user_status = None
        self.office_count_label.configure(text=f"🏢 Office: {self.office_count_val}")
        self.wfh_count_label.configure(text=f"🏠 WFH: {self.wfh_count_val}")
        if hasattr(self, 'status_selector'):
            self.status_selector.set("")


if __name__ == "__main__":
    app = TeamsUI()
    app.mainloop()