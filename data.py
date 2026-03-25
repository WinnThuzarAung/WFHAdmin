from datetime import datetime

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

members = ["Jamie D.", "Alice Chen", "Bob Wang", "Carol Lee"]
activity_log = []

def add_activity(message):
    activity_log.insert(0, f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - {message}")
