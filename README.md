# Backend Assignments

This repository contains my backend development assignments, where I built and improved a **Task Management REST API** using FastAPI.

The project was completed in two stages: first building CRUD operations using in-memory data, and then integrating a SQLite database for persistent data storage.

## 📌 Assignments

### 1. CRUD API Without Database

Built a basic **Task Management API** using FastAPI.

The tasks were initially stored in a Python list, allowing me to understand the fundamentals of:

* REST APIs
* HTTP methods
* CRUD operations
* API endpoints
* Request and response handling

### 2. CRUD API With SQLite Database

Extended the previous API by integrating a **SQLite database**.

Tasks are now stored permanently in a `task.db` database instead of a temporary Python list.

This assignment helped me learn:

* SQLite
* SQL queries
* Database tables
* CRUD operations with a database
* Connecting FastAPI with SQLite
* Persistent data storage

## 🛠️ Technologies

* Python
* FastAPI
* Uvicorn
* SQLite
* SQL
* Git & GitHub
* VS Code

## 📂 Project Structure

```text
backend-assignments/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── task.db
│
└── screenshots/
    ├── get-tasks.png
    ├── post-task.png
    ├── update-task.png
    └── delete-task.png
```

## 🚀 How to Run

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI application:

```bash
uvicorn main:app --reload
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## 📚 Learning Outcome

These assignments helped me understand the progression from a **basic in-memory CRUD API** to a **database-backed REST API** using FastAPI and SQLite.

## 👨‍💻 Author

**Mohd Zaid**

Aspiring AI/ML Engineer | Backend AI Engineering
