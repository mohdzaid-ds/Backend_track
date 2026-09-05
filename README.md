# Backend Development Assignments

This repository contains my backend development assignments and projects completed as part of my learning journey in **Backend AI Engineering**.

The assignments focus on building REST APIs, understanding CRUD operations, working with databases, and using Git/GitHub for version control.

---

## 🚀 Technologies Used

* Python
* FastAPI
* Uvicorn
* SQLite
* SQL
* Git
* GitHub
* VS Code

---

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

> The `venv` folder is not included in the repository because virtual environments should not be committed to GitHub.

---

# 📌 Assignment 1 — FastAPI CRUD API

## Objective

Build a simple **To-Do Task API** using FastAPI.

The API allows users to create, read, update, and delete tasks.

---

## 🔹 API Endpoints

| Method | Endpoint      | Description                   |
| ------ | ------------- | ----------------------------- |
| GET    | `/`           | Check that the API is running |
| GET    | `/health`     | Health check                  |
| GET    | `/tasks`      | Get all tasks                 |
| GET    | `/tasks/{id}` | Get a specific task           |
| POST   | `/tasks`      | Create a new task             |
| PUT    | `/tasks/{id}` | Update a task                 |
| DELETE | `/tasks/{id}` | Delete a task                 |

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

### 2. Open the project

```bash
cd backend-assignments
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Start the FastAPI server

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## 📖 API Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can use Swagger UI to test the API endpoints.

---

# 🗄️ SQLite Database

The project uses **SQLite** to store tasks.

Database file:

```text
task.db
```

The database contains a `tasks` table.

Example task:

```json
{
    "id": 1,
    "title": "Learn FastAPI",
    "done": false
}
```

The API communicates with the database to perform CRUD operations.

---

# 🔄 CRUD Operations

### Create

```text
POST /tasks
```

Creates a new task.

### Read

```text
GET /tasks
```

Returns all tasks.

### Update

```text
PUT /tasks/{id}
```

Updates an existing task.

### Delete

```text
DELETE /tasks/{id}
```

Deletes a task.

---

# 🧪 Testing

The API was tested using FastAPI's Swagger UI.

Screenshots of the API testing process are available in:

```text
screenshots/
```

The screenshots demonstrate:

* Getting tasks
* Creating a task
* Updating a task
* Deleting a task

---

# 📚 What I Learned

Through these assignments, I learned:

* Basics of backend development
* How REST APIs work
* FastAPI application structure
* HTTP methods
* CRUD operations
* API endpoint creation
* Request and response handling
* SQLite database integration
* SQL queries
* Connecting an API with a database
* Testing APIs using Swagger UI
* Using virtual environments
* Managing dependencies with `requirements.txt`
* Git and GitHub workflow

---

# 🔮 Future Improvements

Some possible improvements for this project are:

* Add Pydantic models for request validation
* Add better error handling
* Add authentication and authorization
* Add search and filtering
* Add pagination
* Use PostgreSQL instead of SQLite
* Add automated tests
* Deploy the API online
* Add Docker support

---

## 👨‍💻 Author

**Mohd Zaid**

Aspiring AI/ML Engineer | Backend AI Engineering

---

## ⭐ Project Status

**Completed**

This repository represents my progress in learning backend development and building AI-ready backend applications.
  
