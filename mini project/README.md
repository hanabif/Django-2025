# 📝 CLI Todo Application

A command-line todo application built with Python that uses Object-Oriented Programming (OOP) principles and JSON for data persistence.

## 🎯 Features

- ✅ **Add Todo**: Create new tasks with a title
- 📋 **View Todos**: Display all tasks with ID, title, and completion status
- ✏️ **Update Todo Title**: Change the title of existing tasks
- ✔️ **Toggle Completion**: Mark tasks as completed or pending
- 🗑️ **Delete Todo**: Remove tasks by ID
- 💾 **Data Persistence**: All tasks are automatically saved to `todos.json` and reload when the app restarts

## 🛠️ Technical Stack

- **Language**: Python 3.10+
- **Data Storage**: JSON file (`todos.json`)
- **Design Pattern**: Object-Oriented Programming (OOP)
- **Libraries**: 
  - `json` - JSON serialization/deserialization
  - `dataclasses` - Clean class definitions
  - `pathlib` - File path handling
  - `typing` - Type hints

## 📋 Requirements

- Python 3.10 or higher

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cli-todo-app.git
cd cli-todo-app
```
### 2. Verify Python Installation

```bash
python --version
# or
python3 --version
```
### 3. Run the Application

```bash
python todo_app.py
# or
python3 todo_app.py
```
## 🔄 JSON Serialization & Deserialization
### How Data Persistence Works

This application converts Python objects to JSON and back to ensure your todos persist between sessions.

### Serialization (Python → JSON)
When you add, update, or delete a task, the app converts Task objects into JSON format:

``` bash
# Python Task object
task = Task(id=1, title="Buy groceries", completed=False)

# Converts to Python dictionary
task_dict = task.to_dict()  
# Result: {"id": 1, "title": "Buy groceries", "completed": false}

# Saves to JSON file
json.dumps(task_dict)
```
What happens:

- The Task.to_dict() method uses dataclasses.asdict() to convert the Task object to a dictionary
- The TodoApp._save() method converts all Task objects to dictionaries
- json.dumps() serializes the list of dictionaries into JSON format
- The JSON string is written to todos.json

## Deserialization (JSON → Python)

When the app starts, it loads data from todos.json and converts it back to Task objects:

```bash
# Read JSON file
raw_data = json.loads(file_content)  
# Result: [{"id": 1, "title": "Buy groceries", "completed": false}, ...]

# Convert each dictionary to a Task object
tasks = [Task.from_dict(item) for item in raw_data]
```

What happens:

- The TodoApp._load() method reads the todos.json file
- json.loads() deserializes the JSON string into Python dictionaries
- The Task.from_dict() static method converts each dictionary back into a Task object
- All Task objects are stored in self.tasks list


## 👤 Author
Haymanot Aweke

GitHub: @hanabif

## 🙏 Acknowledgments
Built as part of a CLI application project
Uses Python's built-in libraries for simplicity and efficiency