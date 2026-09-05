# Task API — FastAPI CRUD

A simple **CRUD API** built with **Python and FastAPI** as part of the **FlyRank Internship — Backend Track, Week 2, Assignment A1**.

The API manages a to-do task list and supports the four basic CRUD operations:

* **Create** tasks
* **Read** tasks
* **Update** tasks
* **Delete** tasks

The project uses an **in-memory list** instead of a database, as required by the assignment.

---

## 📌 Project Overview

This project demonstrates the fundamentals of building a backend API using FastAPI.

The API provides endpoints for:

| Operation    | HTTP Method | Endpoint      | Description                      |
| ------------ | ----------- | ------------- | -------------------------------- |
| Create       | `POST`      | `/tasks`      | Create a new task                |
| Read         | `GET`       | `/tasks`      | Get all tasks                    |
| Read         | `GET`       | `/tasks/{id}` | Get a single task                |
| Update       | `PUT`       | `/tasks/{id}` | Update an existing task          |
| Delete       | `DELETE`    | `/tasks/{id}` | Delete a task                    |
| Health Check | `GET`       | `/health`     | Check whether the API is running |

The assignment requires full CRUD functionality, correct HTTP status codes, input validation, Swagger UI, and GitHub publication.

---

## 🛠️ Technologies Used

* **Python 3**
* **FastAPI**
* **Uvicorn**
* **HTTP / REST**
* **JSON**
* **Git**
* **GitHub**
* **Swagger UI / OpenAPI**

---

## 📁 Project Structure

```text
task-api/
│
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
└── screenshots/
    └── swagger-ui.png
```

> Your actual filenames can be different. If your Python file is named something other than `main.py`, replace `main` in the Uvicorn command below.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project directory:

```bash
cd task-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the API

Start the FastAPI server with:

```bash
uvicorn main:app --reload
```

The API will run locally at:

```text
http://127.0.0.1:8000
```

FastAPI also provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

# 📚 API Endpoints

## 1. Root Endpoint

### `GET /`

Returns basic information about the API.

### Example response

```json
{
    "name": "Task API",
    "version": "1.0",
    "endpoints": ["/tasks"]
}
```

---

## 2. Health Check

### `GET /health`

Checks whether the API is running.

### Example response

```json
{
    "status": "ok"
}
```

---

# 🔵 READ — Get All Tasks

## `GET /tasks`

Returns all tasks currently stored in the application.

### Example response

```json
[
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": false
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": false
    },
    {
        "id": 3,
        "title": "Explore SQLite",
        "done": false
    }
]
```

---

# 🔵 READ — Get One Task

## `GET /tasks/{id}`

Returns a specific task using its ID.

### Example

```text
GET /tasks/1
```

### Response

```json
{
    "id": 1,
    "title": "Learn FastAPI",
    "done": false
}
```

### Task Not Found

If the requested ID does not exist, the API returns:

**Status Code:** `404 Not Found`

Example:

```json
{
    "error": "Task 99 not found"
}
```

The assignment specifically requires an unknown task ID to return `404` rather than an empty successful response.

---

# 🟢 CREATE — Create a Task

## `POST /tasks`

Creates a new task.

### Request Body

```json
{
    "title": "Buy milk"
}
```

The API automatically:

1. Generates the next available ID.
2. Sets `done` to `false`.
3. Adds the task to the in-memory list.
4. Returns the newly created task.

### Response

**Status Code:** `201 Created`

```json
{
    "id": 4,
    "title": "Buy milk",
    "done": false
}
```

The assignment requires `POST /tasks` to return `201` when a task is successfully created.

### Validation

An empty or missing title should return:

**Status Code:** `400 Bad Request`

Example:

```json
{
    "error": "Title is required"
}
```

---

# 🟡 UPDATE — Update a Task

## `PUT /tasks/{id}`

Updates an existing task.

### Example Request

```text
PUT /tasks/1
```

### Request Body

```json
{
    "title": "Learn FastAPI",
    "done": true
}
```

### Example Response

```json
{
    "id": 1,
    "title": "Learn FastAPI",
    "done": true
}
```

### Possible Status Codes

| Status Code | Meaning                       |
| ----------- | ----------------------------- |
| `200`       | Task successfully updated     |
| `400`       | Invalid or empty request body |
| `404`       | Task does not exist           |

The assignment requires `PUT` to support changing the task title and/or completion status, with `400` for invalid input and `404` for an unknown ID.

---

# 🔴 DELETE — Delete a Task

## `DELETE /tasks/{id}`

Deletes a task using its ID.

### Example

```text
DELETE /tasks/3
```

### Successful Response

**Status Code:** `204 No Content`

A successful delete returns an empty response body.

### Task Not Found

If the task does not exist:

**Status Code:** `404 Not Found`

```json
{
    "error": "Task 99 not found"
}
```

---

# 📊 HTTP Status Codes Used

| Status Code       | Meaning                 | Used For           |
| ----------------- | ----------------------- | ------------------ |
| `200 OK`          | Request successful      | GET / PUT          |
| `201 Created`     | Resource created        | POST               |
| `204 No Content`  | Successfully deleted    | DELETE             |
| `400 Bad Request` | Invalid input           | POST / PUT         |
| `404 Not Found`   | Resource does not exist | GET / PUT / DELETE |

These are the status codes specified by the assignment requirements.

---

# 🧪 Testing with curl

The API can be tested from the terminal using `curl`.

## Get all tasks

```bash
curl -i http://localhost:8000/tasks
```

## Get one task

```bash
curl -i http://localhost:8000/tasks/1
```

## Create a task

```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\"}"
```

## Update a task

```bash
curl -i -X PUT http://localhost:8000/tasks/1 -H "Content-Type: application/json" -d "{\"title\":\"Learn FastAPI\",\"done\":true}"
```

## Delete a task

```bash
curl -i -X DELETE http://localhost:8000/tasks/1
```

---

# 🧾 Sample `curl -i` Output

The assignment asks for at least one pasted `curl -i` output in the README.

Example:

```text
C:\task-api> curl -i http://localhost:8000/tasks/1

HTTP/1.1 200 OK
content-type: application/json

{
    "id": 1,
    "title": "Learn FastAPI",
    "done": false
}
```

> **Important:** Replace this example with the actual output from your own terminal before submitting.

---

# 📖 Swagger UI

FastAPI automatically generates interactive API documentation using Swagger UI.

After starting the server, open:

```text
http://localhost:8000/docs
```

From Swagger UI, you can test:

* `GET /`
* `GET /health`
* `GET /tasks`
* `GET /tasks/{id}`
* `POST /tasks`
* `PUT /tasks/{id}`
* `DELETE /tasks/{id}`

The assignment requires the complete CRUD cycle to work through Swagger UI's **Try it out** functionality.

## Swagger Screenshot

Add your screenshot here:

```markdown
![Swagger UI](screenshots/swagger-ui.png)
```

Make sure the screenshot clearly shows your API endpoints.

---

# 💾 Data Storage

This project intentionally uses **in-memory storage**.

Tasks are stored in a Python list while the application is running.

There is **no database or file storage** in this version of the project.

This means that if the FastAPI server is stopped or restarted, the tasks created during that session are lost and the original example tasks are loaded again.

This behavior is intentional because the assignment specifies an in-memory list and introduces databases in the following stage/week.

---

# 🔄 CRUD Flow

The complete CRUD workflow is:

```text
        CREATE
          │
          ▼
     POST /tasks
          │
          ▼
        READ
          │
          ▼
     GET /tasks
          │
          ▼
       UPDATE
          │
          ▼
    PUT /tasks/{id}
          │
          ▼
        DELETE
          │
          ▼
   DELETE /tasks/{id}
```

---

# 🎯 Assignment Requirements Checklist

* [x] FastAPI server runs locally
* [x] `GET /` endpoint
* [x] `GET /health` endpoint
* [x] `GET /tasks` endpoint
* [x] `GET /tasks/{id}` endpoint
* [x] `POST /tasks` endpoint
* [x] `PUT /tasks/{id}` endpoint
* [x] `DELETE /tasks/{id}` endpoint
* [x] 404 handling for unknown tasks
* [x] 400 validation for invalid input
* [x] Correct HTTP status codes
* [x] In-memory task storage
* [x] Swagger UI
* [x] CRUD testing with curl
* [x] GitHub repository
* [x] README documentation

---

# 🚀 What I Learned

Through this project, I practiced:

* How APIs work using the request → response cycle
* HTTP methods
* CRUD operations
* FastAPI routing
* Path parameters
* JSON request bodies
* HTTP status codes
* Input validation
* Error handling
* Swagger UI
* OpenAPI documentation
* Testing APIs with `curl`
* Git and GitHub
* Building and documenting a backend application

---

# 🔮 Future Improvements

The current version intentionally uses in-memory storage.

Possible future improvements include:

* SQLite database
* SQLAlchemy
* Search functionality
* Task filtering
* Task statistics
* Pagination
* Persistent data storage
* Authentication and authorization
* Automated API tests

---

# 👨‍💻 Author

**Mohd Zaid**

Aspiring Backend AI Engineer

Built as part of the **FlyRank Internship — Backend Track — Week 2 — Assignment A1**.

---

## 📌 Assignment

**FlyRank Internship**
**Backend Track — Week 2 — Assignment A1**
**Build Your First CRUD API**

The goal of this assignment was to build a small to-do API supporting Create, Read, Update, and Delete operations, test it through Swagger UI, and publish it to GitHub.
