import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List


@dataclass
class Task:
    id: int
    title: str
    completed: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Task":
        return Task(
            id=int(data.get("id", 0)),
            title=str(data.get("title", "")),
            completed=bool(data.get("completed", False)),
        )


class TodoApp:
    def __init__(self, storage_path: Path):
        self.storage_path = Path(storage_path)
        self.tasks: List[Task] = []
        self._load()

    def _load(self) -> None:
        if not self.storage_path.exists():
            self.storage_path.write_text("[]", encoding="utf-8")
            return
        try:
            raw = json.loads(self.storage_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            print("Could not read todos.json. Starting with an empty list.")
            raw = []
        if isinstance(raw, list):
            self.tasks = [Task.from_dict(item) for item in raw if self._valid_task_dict(item)]
        else:
            self.tasks = []

    def _save(self) -> None:
        payload = [task.to_dict() for task in self.tasks]
        self.storage_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @staticmethod
    def _valid_task_dict(item: dict) -> bool:
        return isinstance(item, dict) and "id" in item and "title" in item

    def _next_id(self) -> int:
        return max((task.id for task in self.tasks), default=0) + 1

    def add_task(self, title: str) -> Task:
        clean_title = title.strip()
        if not clean_title:
            raise ValueError("Title cannot be empty.")
        task = Task(id=self._next_id(), title=clean_title, completed=False)
        self.tasks.append(task)
        self._save()
        return task

    def list_tasks(self) -> List[Task]:
        return sorted(self.tasks, key=lambda t: t.id)


def display_tasks(tasks: List[Task]) -> None:
    if not tasks:
        print("No todos yet.")
        return
    print("\nSaved Todos:")
    for task in tasks:
        status = "Done" if task.completed else "Pending"
        print(f"[{task.id}] {task.title} - {status}")


def main() -> None:
    storage_path = Path(__file__).parent / "todos.json"
    app = TodoApp(storage_path)

    while True:
        print("\nTodo App")
        print("1. Add Todo")
        print("2. View Todos")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Enter todo title: ").strip()
            try:
                task = app.add_task(title)
                print(f"Added todo with ID {task.id}.")
            except ValueError as exc:
                print(exc)

        elif choice == "2":
            display_tasks(app.list_tasks())

        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
