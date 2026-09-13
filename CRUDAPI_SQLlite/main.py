from fastapi import FastAPI, HTTPException
from database import get_connection, create_database


app = FastAPI()


# Create the database and table when the application starts
@app.on_event("startup")
def startup():
    create_database()


# -------------------------
# ROOT
# -------------------------

@app.get("/")
def root():
    return {
        "message": "FastAPI CRUD API with SQLite"
    }


# -------------------------
# GET ALL TASKS
# -------------------------

@app.get("/tasks")
def get_tasks():
    connection = get_connection()

    cursor = connection.execute("""
        SELECT id, title, done
        FROM tasks
        ORDER BY id
    """)

    tasks = []

    for row in cursor.fetchall():
        tasks.append({
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        })

    connection.close()

    return tasks


# -------------------------
# GET ONE TASK
# -------------------------

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    connection = get_connection()

    cursor = connection.execute("""
        SELECT id, title, done
        FROM tasks
        WHERE id = ?
    """, (task_id,))

    row = cursor.fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }


# -------------------------
# CREATE TASK
# -------------------------

@app.post("/tasks")
def create_task(task: dict):
    if "title" not in task:
        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )

    title = task["title"]
    done = task.get("done", False)

    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO tasks (title, done)
        VALUES (?, ?)
    """, (title, int(done)))

    connection.commit()

    task_id = cursor.lastrowid

    connection.close()

    return {
        "id": task_id,
        "title": title,
        "done": bool(done)
    }


# -------------------------
# UPDATE TASK
# -------------------------

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: dict):
    connection = get_connection()

    # Check whether task exists
    cursor = connection.execute("""
        SELECT id
        FROM tasks
        WHERE id = ?
    """, (task_id,))

    existing_task = cursor.fetchone()

    if existing_task is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if "title" not in task:
        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )

    title = task["title"]
    done = task.get("done", False)

    connection.execute("""
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
    """, (title, int(done), task_id))

    connection.commit()
    connection.close()

    return {
        "id": task_id,
        "title": title,
        "done": bool(done)
    }


# -------------------------
# DELETE TASK
# -------------------------

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    connection = get_connection()

    cursor = connection.execute("""
        SELECT id
        FROM tasks
        WHERE id = ?
    """, (task_id,))

    existing_task = cursor.fetchone()

    if existing_task is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    connection.execute("""
        DELETE FROM tasks
        WHERE id = ?
    """, (task_id,))

    connection.commit()
    connection.close()

    return {
        "message": "Task deleted successfully"
    }