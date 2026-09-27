Containerize Your Stack --- FastAPI + PostgreSQL

A containerized task management REST API built with FastAPI and
PostgreSQL.
This assignment evolves the task API from in-memory storage to a real
PostgreSQL database and finally runs the complete application stack with
Docker Compose.

Tech Stack

Python 3.12

FastAPI

Uvicorn

PostgreSQL 16

psycopg

Docker

Docker Compose

Project Structure

CRUD_with_database/
│
├── main.py
├── database.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .env
├── .env.example
├── .gitignore
└── README.md

Adjust the filenames above if your actual project uses different
module names.

Features

Create, read, update, and delete tasks

PostgreSQL database persistence

Parameterized SQL queries

Environment-based database configuration

Dockerized FastAPI application

Dockerized PostgreSQL database

Docker Compose for running the complete stack

Persistent PostgreSQL storage through a Docker volume

Interactive FastAPI Swagger documentation

Database Configuration

Create a .env file locally:

DATABASE_URL=postgresql://postgres:dev@db:5432/tasks

For local development outside Docker, the database host may need to be
changed from db to localhost.

Never commit .env to GitHub.

The repository should contain .env.example instead:

DATABASE_URL=postgresql://postgres:dev@db:5432/tasks

Running the Application with Docker Compose

Make sure Docker Desktop is running.

Build and start the complete stack:

docker compose up --build

The application should then be available at:

http://localhost:8000

Swagger UI:

http://localhost:8000/docs

To run the containers in the background:

docker compose up --build -d

To stop the stack:

docker compose down

API Endpoints

Method   Endpoint        Description        Expected Status

GET      /             API status         200
GET      /tasks        Get all tasks      200
GET      /tasks/{id}   Get a task by ID   200 / 404
POST     /tasks        Create a task      201 / 400
PUT      /tasks/{id}   Update a task      200 / 400 / 404
DELETE   /tasks/{id}   Delete a task      204 / 404

Example Requests

Get all tasks

curl -i http://localhost:8000/tasks

Get one task

curl -i http://localhost:8000/tasks/1

Create a task

curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Learn Docker\"}"

Update a task

curl -i -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Learn Docker Compose\",\"done\":true}"

Delete a task

curl -i -X DELETE http://localhost:8000/tasks/1

PostgreSQL

The application uses PostgreSQL instead of an in-memory list or SQLite
database.

The PostgreSQL service runs inside Docker and is accessed by the API
through the Compose service name:

db

Inside the Docker Compose network, the API should not use:

localhost

Instead, it connects to PostgreSQL using:

db:5432

Persistence

PostgreSQL data is stored in a Docker named volume.

This means database data should survive:

docker compose down

followed by:

docker compose up

The containers may be recreated, but the database volume preserves the
stored tasks.

Database Verification

List running containers:

docker compose ps

Open a PostgreSQL shell:

docker compose exec db psql -U postgres -d tasks

List tables:

\dt

View tasks:

SELECT * FROM tasks;

Exit PostgreSQL:

\q

Environment Variables

Variable Purpose

DATABASE_URL   PostgreSQL connection string

Example:

DATABASE_URL=postgresql://postgres:dev@db:5432/tasks

Security

Sensitive environment files must not be committed.

The .gitignore file should contain at least:

.env
.venv/
venv/
__pycache__/
*.pyc

Use .env.example to document required environment variables without
exposing real secrets.

Docker Commands

Build the application image:

docker compose build

Start the complete stack:

docker compose up

Stop the stack:

docker compose down

View logs:

docker compose logs

View API logs:

docker compose logs api

View database logs:

docker compose logs db

Check container status:

docker compose ps

Assignment Stages

Stage 0 --- PostgreSQL in Docker

Run PostgreSQL in a Docker container

Configure the database

Create the required .gitignore

Verify PostgreSQL connectivity

Stage 1 --- Connect FastAPI to PostgreSQL

Configure DATABASE_URL

Install the PostgreSQL driver

Connect the API to PostgreSQL

Create the tasks table

Seed initial tasks when the table is empty

Stage 2 --- Read from PostgreSQL

Implement:

GET /tasks
GET /tasks/{id}

Use parameterized SQL queries and return 404 for an unknown task ID.

Stage 3 --- Full CRUD

Implement:

POST /tasks
PUT /tasks/{id}
DELETE /tasks/{id}

Validate incoming data and use parameterized SQL queries.

Stage 4 --- Docker Compose

Containerize both:

FastAPI application
        ↓
PostgreSQL

Run both services with:

docker compose up

Use a persistent PostgreSQL volume.

Stage 5 --- GitHub and Documentation

The repository should contain:

Source code

Dockerfile

Compose configuration

.env.example

.gitignore

README



