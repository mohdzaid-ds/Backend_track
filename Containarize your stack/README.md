# PostgreSQL + Docker Compose

## Overview

This project extends the A2 service by replacing its in-memory data storage with PostgreSQL running in Docker.

The application follows a layered architecture in which the service layer communicates with a repository abstraction rather than directly depending on the database implementation.

This makes it possible to replace the in-memory repository with a PostgreSQL repository while keeping the **service and API routes unchanged**.

The complete application stack can be started with a single command:

```bash
docker compose up
```

---

## Objectives

This assignment demonstrates how to:

* Run PostgreSQL using Docker
* Persist database data using a Docker volume
* Store database configuration in environment variables
* Keep sensitive configuration out of Git
* Provide a safe `.env.example`
* Create database tables using SQL
* Implement a PostgreSQL repository
* Replace the in-memory repository without changing the service or routes
* Run the application and database together with Docker Compose
* Verify data persistence across container restarts

---

## Architecture

The application uses a layered architecture:

```text
Client
   │
   ▼
FastAPI Routes
   │
   ▼
Service Layer
   │
   ▼
Repository Interface
   │
   ▼
PostgreSQL Repository
   │
   ▼
PostgreSQL
   │
   ▼
Docker Volume
```

### Storage abstraction

The original implementation used an in-memory repository:

```text
Service
   │
   ▼
In-Memory Repository
   │
   ▼
Application Memory
```

This assignment replaces it with:

```text
Service
   │
   ▼
PostgreSQL Repository
   │
   ▼
PostgreSQL
```

The repository abstraction allows the storage implementation to change without requiring changes to the service or API route layers.

---

## Project Structure

```text
project/
│
├── main.py
├── database.py
├── requirements.txt
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

> The exact filenames may vary depending on the existing A2 implementation.

---

## Technology Stack

* **Python**
* **FastAPI**
* **PostgreSQL**
* **Docker**
* **Docker Compose**
* **SQL**
* **Environment Variables**
* **Repository Pattern**

---

## Environment Configuration

Database configuration is loaded from environment variables.

The real `.env` file is intentionally excluded from version control.

### `.env`

The local `.env` file should contain the actual database connection information.

Example structure:

```env
DATABASE_URL=postgresql://<username>:<password>@db:5432/<database_name>
```

The values shown above are placeholders only.

### `.env.example`

The repository contains a safe template:

```env
DATABASE_URL=postgresql://<username>:<password>@db:5432/<database_name>
```

No real credentials should be placed in this file.

### `.gitignore`

The following sensitive/local files should be ignored:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

**Important:** Never commit real database passwords, API keys, access tokens, or other secrets to GitHub.

---

## Database Schema

The database schema is defined in:

```text
schema.sql
```

The SQL file is responsible for creating the required database table.

Example:

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);
```

Using `IF NOT EXISTS` prevents the command from failing when the table already exists.

---

## PostgreSQL Repository

The PostgreSQL repository implements the same repository interface used by the application.

Its responsibility is to handle database operations such as:

* Creating records
* Retrieving records
* Updating records
* Deleting records

The service layer does not need to know whether the data is stored in memory or PostgreSQL.

### Repository abstraction

```text
Repository Interface
        │
        ├── In-Memory Repository
        │
        └── PostgreSQL Repository
```

For this assignment, the PostgreSQL implementation is used by the application.

---

## Service and API Routes

A key requirement of this assignment is that the **service and API routes remain unchanged** when switching storage implementations.

The resulting flow is:

```text
HTTP Request
     │
     ▼
FastAPI Route
     │
     ▼
Service Layer
     │
     ▼
Repository Interface
     │
     ▼
PostgreSQL Repository
     │
     ▼
PostgreSQL
```

Only the storage implementation is changed.

This demonstrates the practical benefit of separating business logic from persistence logic.

---

# Docker

## PostgreSQL Container

PostgreSQL runs inside a Docker container.

A named Docker volume is attached to the PostgreSQL data directory:

```yaml
volumes:
  postgres_data:
```

The database service mounts the volume:

```yaml
services:
  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

The volume allows database data to survive when the PostgreSQL container itself is stopped or recreated.

---

## Docker Compose

The `docker-compose.yml` file defines the complete local stack:

```text
Docker Compose
│
├── FastAPI Application
│
└── PostgreSQL Database
        │
        └── Persistent Volume
```

The application connects to PostgreSQL through the Docker Compose network.

---

## Running the Application

Make sure Docker Desktop is running.

From the project directory:

```bash
docker compose up
```

To start the stack in detached mode:

```bash
docker compose up -d
```

Check the running services:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs
```

---

## API Documentation

When the FastAPI application is running, the interactive Swagger documentation is available at:

```text
http://localhost:8000/docs
```

This address is local to the development environment and does not contain any confidential information.

---

# Persistence Verification

The purpose of using a PostgreSQL volume is to ensure that application data survives container restarts.

The persistence test follows this process:

### 1. Start the stack

```bash
docker compose up -d
```

### 2. Create records

Use the API to create one or more records.

For example:

```text
POST /tasks
```

### 3. Verify the records

Retrieve the records:

```text
GET /tasks
```

Confirm that the newly created records are present.

### 4. Stop the containers

```bash
docker compose down
```

### 5. Start the stack again

```bash
docker compose up -d
```

### 6. Retrieve the records again

```text
GET /tasks
```

The previously created records should still be present.

This demonstrates that the PostgreSQL data is stored in the Docker volume rather than being tied to the lifecycle of the PostgreSQL container.

> Only mark this verification as completed after performing the test locally.

---

## Useful Docker Commands

### Start the stack

```bash
docker compose up
```

### Start in the background

```bash
docker compose up -d
```

### Check services

```bash
docker compose ps
```

### View logs

```bash
docker compose logs
```

### Stop containers

```bash
docker compose down
```

### List Docker volumes

```bash
docker volume ls
```

### Stop containers and remove the database volume

```bash
docker compose down -v
```

> **Warning:** `docker compose down -v` removes the PostgreSQL volume and therefore deletes the persisted database data.

---

# Requirements Checklist

| Requirement                 | Implementation                        |
| --------------------------- | ------------------------------------- |
| PostgreSQL runs in Docker   | PostgreSQL Docker service             |
| Persistent database         | Docker named volume                   |
| Environment configuration   | `.env`                                |
| Secrets excluded from Git   | `.gitignore`                          |
| Safe configuration template | `.env.example`                        |
| Database table              | `schema.sql`                          |
| PostgreSQL repository       | Repository implementation             |
| Service unchanged           | Repository abstraction                |
| Routes unchanged            | Existing FastAPI routes               |
| Complete stack              | Docker Compose                        |
| Single startup command      | `docker compose up`                   |
| Persistence verification    | Restart and re-check database records |

---

# Security

This repository is designed to avoid committing confidential configuration.

### Never commit:

* Database passwords
* API keys
* Access tokens
* JWT secrets
* Private keys
* Production credentials
* Personal `.env` files

### Safe to commit:

* `.env.example`
* `schema.sql`
* `Dockerfile`
* `docker-compose.yml` containing only non-secret configuration
* Python source code
* `requirements.txt`
* `.gitignore`
* `README.md`

Before pushing the project to GitHub, verify the repository does not contain sensitive values.

---

# Key Learning

This assignment demonstrates why a repository abstraction is useful in backend application development.

The application can move from:

```text
In-Memory Storage
```

to:

```text
PostgreSQL Storage
```

without rewriting the service or API routes.

Docker provides a reproducible PostgreSQL environment, Docker Compose manages the application and database together, and the persistent volume ensures that database records survive container restarts.

The final stack can be started with:

```bash
docker compose up
```

---

## Conclusion

The A2 service has been extended from an in-memory implementation to a persistent PostgreSQL-backed application.

The resulting setup provides:

* Layered application architecture
* Repository-based storage abstraction
* PostgreSQL persistence
* Dockerized database infrastructure
* Environment-based configuration
* Docker volume persistence
* Docker Compose orchestration
* A single command for starting the local stack

This establishes a practical foundation for future backend features such as background jobs, caching, queues, and retrieval-augmented generation (RAG).
