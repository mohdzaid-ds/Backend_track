from fastapi import FastAPI , HTTPException
from database import engine, initialize_database, get_all_tasks, get_task_by_id, create_task ,update_task as update_task_db,delete_task as delete_task_db

app = FastAPI()


@app.on_event("startup")
def startup():
    initialize_database()


@app.get("/")
def root():
    return {"message": "FastAPI + PostgreSQL is working"}

@app.get("/test-db")
def test_db():
    try:
        with engine.connect():
            return {"database": "PostgreSQL connection successful"}
    except Exception as e:
        return {"database": "Connection failed", "error": str(e)}

@app.get("/tasks")
def get_tasks():
    return get_all_tasks()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

@app.post("/tasks", status_code=201)
def add_task(task: dict):
    if "title" not in task or not task["title"].strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )

    title = task["title"]
    done = task.get("done", False)

    return create_task(title, done)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: dict):
    if "title" not in task or not task["title"].strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )

    title = task["title"]
    done = task.get("done", False)

    updated_task = update_task_db(task_id, title, done)

    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return updated_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    deleted_task = delete_task_db(task_id)

    if deleted_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return deleted_task