import csv
import os
from datetime import datetime
from task_manager import Task

class Storage:

    def __init__(self):
        self.filename = "tasks.csv"
        self.file_exists()

    def file_exists(self):
        if not os.path.isfile(self.filename):
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['title', 'description', 'completed', 'created_at', 'completed_at'])

    def read_tasks(self):
        tasks = []
        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tasks.append(Task(
                    title=row['title'],
                    description=row['description'],
                    completed=row['completed'] == 'True',
                    created_at=row['created_at'],
                    completed_at=row['completed_at'] if row['completed_at'] != 'None' else None
                ))
        return tasks

    def write_tasks(self, tasks):
        with open(self.filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['title', 'description', 'completed', 'created_at', 'completed_at'])
            for task in tasks:
                writer.writerow([
                    task.title,
                    task.description,
                    task.completed,
                    task.created_at,
                    task.completed_at or 'None'
                ])

    def save_task(self, task):
        tasks = self.read_tasks()
        tasks.append(task)
        self.write_tasks(tasks)

    def update_task(self, updated_task):
        tasks = self.read_tasks()
        found = False
        for i in range(len(tasks)):
            if tasks[i].title == updated_task.title:
                tasks[i] = updated_task
                found = True
                break
        if found:
            self.write_tasks(tasks)

    def get_task(self, title):
        tasks = self.read_tasks()
        for task in tasks:
            if task.title == title:
                return task
        return None

    def get_all_tasks(self):
        return self.read_tasks()

    def clear_all_tasks(self):
        self.write_tasks([])
