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

    def find_task_by_id(self, task_id: int) -> Task | None:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise ValueError(f"Task with ID {task_id} not found.")

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

    def update_task_title(self, task_id: int, new_title:str) -> None:
        del_task = self.find_task_by_id(task_id)
        if not del_task:
            raise ValueError(f"Task with ID {task_id} not found.") 
        new_title = new_title.strip()
        if not new_title:
            raise ValueError("Title cannot be empty.")
        del_task.title = new_title
        self._save()

    def toggle_compl(self, task_id: int) -> None:
        task =self.find_task_by_id(task_id)
        if task is None:
            raise ValueError("Task not found")
        task.completed  = not task.completed
        self._save()
    
    def delete_task(self, task_id: int) -> None:
        task = self.find_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found.")
        
        self.tasks.remove(task)  
        self._save()


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
        print("3. Update Todos")
        print("4. Toggle completion")
        print("5. Delete Todo")
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
        elif choice == '3':
            try:
                task_id = int(input("Enter task ID: ".strip()))
                new_title = input("enter new titile: ").strip()
                app.update_task_title(task_id, new_title)
                print(f'updated task {task_id}')
            except ValueError as exc:
                print(exc)
        elif choice == "4":
            try:
                task_id = int(input("Enter task ID to toggle: ").strip())
                app.toggle_compl(task_id)
                print(f"Toggled completion status for task {task_id}.")
            except ValueError as exc:
                print(exc)
        elif choice == "5":
            try:
                task_id = int(input("Enter task ID to delete: ").strip())
                app.delete_task(task_id)
                print(f"Deleted task {task_id}.")
            except ValueError as exc:
                print(exc)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")



if __name__ == "__main__":
    main()
