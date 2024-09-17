from datetime import datetime, timedelta

class Task:

    def __init__(self, title, description, completed=False, created_at=None, completed_at=None):
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()
        self.completed_at = completed_at

class TaskManager:

    def __init__(self, storage):
        self.storage = storage

    def add_task(self, title, description):
        task = Task(title, description)
        self.storage.save_task(task)
        return task

    def complete_task(self, title):
        task = self.storage.get_task(title)
        if task:
            task.completed = True
            task.completed_at = datetime.now().isoformat()
            self.storage.update_task(task)
            return True
        return False

    def list_tasks(self, include_completed=False):
        tasks = self.storage.get_all_tasks()
        if not include_completed:
            tasks = [task for task in tasks if not task.completed]
        return tasks

    def generate_report(self):
        tasks = self.storage.get_all_tasks()
        total_tasks = len(tasks)
        completed_tasks = []
        for task in tasks:
            if task.completed and task.completed_at:
                completed_tasks.append(task)

        if completed_tasks:
            total_seconds = 0
            for task in completed_tasks:
                created_at = datetime.fromisoformat(task.created_at)
                completed_at = datetime.fromisoformat(task.completed_at)
                time_diff = completed_at - created_at
                total_seconds += time_diff.total_seconds()
            average_time = total_seconds / len(completed_tasks)
        else:
            average_time = 0

        report = {
            "total": total_tasks,
            "completed": len(completed_tasks),
            "pending": total_tasks - len(completed_tasks),
            "average_time_to_complete": average_time
        }

        return report
