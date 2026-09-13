# W3 · A1 --- Connecting your CRUD to the Database

## Overview

This project is the Week 3 Backend Track assignment from the FlyRank
internship.

The goal of this assignment was to take the CRUD API built in the
previous assignment and replace the in-memory task list with a real
**SQLite database**.

The API endpoints continue to work with the same basic CRUD behavior,
but the task data is now stored permanently in a local database file.

### Before

``` text
Client → FastAPI → In-memory task list
```

### After

``` text
Client → FastAPI → SQLite Database
```

The main improvement is that task data survives when the FastAPI server
is restarted.

------------------------------------------------------------------------

## Tech Stack

-   **Language:** Python
-   **Framework:** FastAPI
-   **Database:** SQLite
-   **Database Library:** sqlite3
-   **API Documentation:** Swagger UI
-   **Testing:** FastAPI Swagger UI / browser
-   **Database File:** `tasks.db`

SQLite does not require a separate database server. The database is
stored in a single local file.

------------------------------------------------------------------------

## Project Structure

``` text
CRUD_with_database/
│
├── main.py
├── database.py
├── tasks.db
├── requirements.txt
├── README.md
├── .gitignore
│
└── screenshots/
    └── database.png
```

> `tasks.db` is the SQLite database created by the application.

------------------------------------------------------------------------

## Database Structure

The application creates a table named `tasks`.

  Column    Type      Description
  --------- --------- -------------------
  `id`      INTEGER   Primary key
  `title`   TEXT      Task title
  `done`    BOOLEAN   Completion status

The table is created automatically when the application starts.

If the table is empty, three example tasks are inserted.

The example tasks are inserted only once, so restarting the server does
not duplicate them.

------------------------------------------------------------------------

## API Endpoints

  Method     Endpoint        Description
  ---------- --------------- -------------------------------
  `GET`      `/`             Check that the API is running
  `GET`      `/health`       Health check
  `GET`      `/tasks`        Get all tasks
  `GET`      `/tasks/{id}`   Get one task
  `POST`     `/tasks`        Create a new task
  `PUT`      `/tasks/{id}`   Update a task
  `DELETE`   `/tasks/{id}`   Delete a task

------------------------------------------------------------------------

## CRUD Operations

### Create

``` http
POST /tasks
```

Example request:

``` json
{
  "title": "Learn FastAPI"
}
```

Creates a new task and stores it as a row in the SQLite database.

------------------------------------------------------------------------

### Read All Tasks

``` http
GET /tasks
```

Returns all tasks stored in the database.

------------------------------------------------------------------------

### Read One Task

``` http
GET /tasks/{id}
```

Example:

``` text
GET /tasks/1
```

Returns the task with the requested ID.

If the ID does not exist, the API returns:

``` json
{
  "error": "Task not found"
}
```

with status code `404`.

------------------------------------------------------------------------

### Update

``` http
PUT /tasks/{id}
```

Updates an existing task in the database.

------------------------------------------------------------------------

### Delete

``` http
DELETE /tasks/{id}
```

Deletes the selected task from the database.

------------------------------------------------------------------------

## Status Codes

  Status Code   Meaning       Usage
  ------------- ------------- ---------------------------
  `200`         OK            Successful read or update
  `201`         Created       Successful task creation
  `204`         No Content    Successful deletion
  `400`         Bad Request   Invalid or empty input
  `404`         Not Found     Task ID does not exist

------------------------------------------------------------------------

## Installation

Create and activate a virtual environment:

### Windows PowerShell

``` powershell
python -m venv venv
```

``` powershell
.\venv\Scripts\Activate.ps1
```

Install the required packages:

``` powershell
pip install -r requirements.txt
```

------------------------------------------------------------------------

## Run the Application

Start the FastAPI server with:

``` powershell
uvicorn main:app --reload
```

The API will be available at:

``` text
http://localhost:8000
```

------------------------------------------------------------------------

## Swagger UI

FastAPI automatically provides interactive API documentation.

Open:

``` text
http://localhost:8000/docs
```

Use **Try it out** to test the complete CRUD cycle:

1.  Create a task
2.  List tasks
3.  Retrieve a task
4.  Update a task
5.  Delete a task
6.  Confirm the task is deleted

------------------------------------------------------------------------

## SQLite Persistence Test

One of the main goals of this assignment is to confirm that the data
survives a server restart.

### Test

1.  Start the FastAPI server.
2.  Create a new task.
3.  Run `GET /tasks`.
4.  Stop the server.
5.  Start the server again.
6.  Run `GET /tasks`.

The previously created task should still be present.

This happens because the tasks are stored in `tasks.db` instead of an
in-memory Python list.

------------------------------------------------------------------------

## SQL Queries Practiced

The following SQL queries were used to explore the SQLite database.

### List every task

``` sql
SELECT * FROM tasks;
```

### Show completed tasks

``` sql
SELECT * FROM tasks WHERE done = 1;
```

### Count all tasks

``` sql
SELECT COUNT(*) FROM tasks;
```

### Mark every task as completed

``` sql
UPDATE tasks SET done = 1;
```

### Delete all completed tasks

``` sql
DELETE FROM tasks WHERE done = 1;
```

Changes made directly to the SQLite database are reflected by the API
when the task endpoints are requested again.

------------------------------------------------------------------------

## Database Screenshot

Add the screenshot of the SQLite database viewer here:

``` text
screenshots/database.png
```

Example Markdown:

``` markdown
![SQLite Database](screenshots/database.png)
```

------------------------------------------------------------------------

## What I Learned

Through this assignment, I learned how to:

-   Connect a FastAPI application to SQLite.
-   Create a database and table automatically.
-   Store API data permanently instead of keeping it in memory.
-   Use SQL queries for CRUD operations.
-   Read data from a database through API endpoints.
-   Insert, update, and delete database records.
-   Handle missing task IDs with `404`.
-   Understand how an API layer communicates with a storage layer.
-   Verify database data using a SQLite database viewer.
-   Test persistence by restarting the server.

------------------------------------------------------------------------

## Architecture

``` text
             Client
               │
               ▼
        ┌─────────────┐
        │   FastAPI   │
        │     API     │
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │  database.py│
        │   sqlite3   │
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │   tasks.db  │
        │    SQLite   │
        └─────────────┘
```

The client interacts with the API, while the API uses the database layer
to store and retrieve task data.

------------------------------------------------------------------------

## Assignment Stages

### Stage 0 --- Create SQLite Database

-   Created `tasks.db`
-   Created the `tasks` table
-   Added three example tasks only when the table is empty
-   Verified that restarting the application does not duplicate the
    example tasks

Commit:

``` text
Stage 0: create SQLite database
```

### Stage 1 --- Read from Database

-   Replaced in-memory reads with SQL queries
-   Implemented `GET /tasks`
-   Implemented `GET /tasks/{id}`
-   Added `404` handling for unknown IDs

Commit:

``` text
Stage 1: database read endpoints
```

### Stage 2 --- Create New Tasks

-   Replaced the in-memory append operation with a database `INSERT`
-   Preserved validation behavior
-   Confirmed created tasks remain after restarting the server

Commit:

``` text
Stage 2: insert into database
```

### Stage 3 --- Update and Delete

-   Replaced update logic with SQL `UPDATE`
-   Replaced delete logic with SQL `DELETE`
-   Verified the complete CRUD cycle

Commit:

``` text
Stage 3: update and delete with SQL
```

### Stage 4 --- Explore SQLite

Practiced:

``` sql
SELECT * FROM tasks;
SELECT * FROM tasks WHERE done = 1;
SELECT COUNT(*) FROM tasks;
UPDATE tasks SET done = 1;
DELETE FROM tasks WHERE done = 1;
```

Commit:

``` text
Stage 4: explored SQLite
```

### Stage 5 --- Documentation

-   Updated the README
-   Documented SQLite usage
-   Added database location
-   Added setup and run instructions
-   Added SQL examples
-   Added database viewer screenshot

Commit:

``` text
Stage 5: database documentation
```

------------------------------------------------------------------------

## Key Concept

The most important concept from this assignment is the separation
between the API and the storage layer.

The API describes **what** the application does:

``` text
GET
POST
PUT
DELETE
```

The database describes **where** the application stores its data.

``` text
API → Database
```

This means the client does not need to know whether the application uses
an in-memory list, SQLite, PostgreSQL, or another database.

------------------------------------------------------------------------

## Result

The CRUD API now uses a real SQLite database instead of an in-memory
task list.

The API continues to support:

``` text
Create → Read → Update → Delete
```

while task data persists across server restarts.

