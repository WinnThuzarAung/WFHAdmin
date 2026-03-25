import customtkinter as ctk
from data import tasks, members

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
        # Filter tasks based on mode (mock logic)
        filtered = [t for t in tasks if self.mode == "leader" or t["assigned_to"] == self.current_user]
        for task in filtered:
            frame = ctk.CTkFrame(self.tasks_container, fg_color=("gray95", "gray20"), corner_radius=10)
            frame.pack(fill="x", padx=5, pady=5)
            ctk.CTkLabel(frame, text=task["title"], font=ctk.CTkFont(size=15, weight="bold")).pack(side="left", padx=10)
            ctk.CTkLabel(frame, text=f"Assigned: {task['assigned_to']}").pack(side="left", padx=10)
            ctk.CTkLabel(frame, text=f"Due: {task['end_date']}").pack(side="left", padx=10)

    def show_create_dialog(self):
        # Placeholder for task creation dialog
        pass
