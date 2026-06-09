import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path

import requests

TASKS_FILE = Path("tasks.json")


@dataclass
class Task:
    description: str
    completed: bool = False


class TaskManager:
    def __init__(self, tasks_file: Path = TASKS_FILE):
        self.tasks_file = tasks_file
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        if not self.tasks_file.exists():
            return []
        try:
            payload = json.loads(self.tasks_file.read_text(encoding="utf-8"))
            return [Task(**item) for item in payload]
        except (json.JSONDecodeError, OSError):
            return []

    def _save_tasks(self):
        self.tasks_file.write_text(
            json.dumps([asdict(task) for task in self.tasks], indent=2),
            encoding="utf-8",
        )

    def add_task(self, description: str):
        task = Task(description=description)
        self.tasks.append(task)
        self._save_tasks()
        print(f"Task added: {description}")

    def complete_task(self, task_id: int):
        if task_id < 1 or task_id > len(self.tasks):
            raise IndexError("Task ID out of range")

        task = self.tasks[task_id - 1]
        if task.completed:
            print(f"Task {task_id} is already complete: {task.description}")
            return

        task.completed = True
        self._save_tasks()
        print(f"Task completed: {task_id} - {task.description}")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks available.")
            return

        print("Task list:")
        for index, task in enumerate(self.tasks, start=1):
            status = "[x]" if task.completed else "[ ]"
            print(f"{index}. {status} {task.description}")

    def fetch_sample_task(self):
        url = "https://jsonplaceholder.typicode.com/todos/1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        sample = response.json()
        description = sample.get("title", "Sample task")
        self.add_task(f"{description} (fetched)")


def build_parser():
    parser = argparse.ArgumentParser(
        description="Task CLI tool for adding, completing, and listing tasks."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add-task", help="Add a new task")
    add_parser.add_argument("description", help="Description of the task")

    complete_parser = subparsers.add_parser("complete-task", help="Mark a task complete")
    complete_parser.add_argument("task_id", type=int, help="ID of the task to complete")

    subparsers.add_parser("list-tasks", help="List all tasks")
    subparsers.add_parser("fetch-sample-task", help="Fetch a sample task from a public API")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    manager = TaskManager()

    if args.command == "add-task":
        manager.add_task(args.description)
    elif args.command == "complete-task":
        try:
            manager.complete_task(args.task_id)
        except IndexError as error:
            print(f"Error: {error}")
    elif args.command == "list-tasks":
        manager.list_tasks()
    elif args.command == "fetch-sample-task":
        try:
            manager.fetch_sample_task()
        except requests.RequestException as error:
            print(f"Failed to fetch sample task: {error}")


if __name__ == "__main__":
    main()
