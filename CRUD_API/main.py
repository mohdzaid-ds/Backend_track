from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": False
    },
    {
        "id": 3,
        "title": "Complete FlyRank Assignment",
        "done": False
    }
]


@app.get("/")
def root():
    return{
        "name": "Task API",
        "Version": "1.0",
        "endpoint": "[/tasks]"
    }

@app.get("/health")
def health():
    return{
        "status": "ok"
    }

@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


@app.post("/tasks", status_code=201)
def create_task(task: dict):
    if "title" not in task or not task["title"].strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"}
        )
    
    if not task["title"].strip():
        return JSONResponse(
            status_code=400,
            content={
                "error": "Title is required"
            }
        )

    new_id = max(task["id"] for task in tasks) + 1

    new_task = {
        "id": new_id,
        "title": task["title"],
        "done": False
    }

    tasks.append(new_task)

    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: dict):

    # Validate empty body
    if not task:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Request body cannot be empty"
            }
        )

    # Validate title
    if "title" in task:

        if not isinstance(task["title"], str):
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Title must be a string"
                }
            )

        if not task["title"].strip():
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Title cannot be empty"
                }
            )

    # Validate done
    if "done" in task:

        if not isinstance(task["done"], bool):
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Done must be a boolean"
                }
            )

    # Find and update task
    for existing_task in tasks:

        if existing_task["id"] == task_id:

            if "title" in task:
                existing_task["title"] = task["title"]

            if "done" in task:
                existing_task["done"] = task["done"]

            return existing_task

    # Task not found
    return JSONResponse(
        status_code=404,
        content={
            "error": f"Task {task_id} not found"
        }
    )


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )
