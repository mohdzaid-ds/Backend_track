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


# GET /tasks
@app.get("/tasks")
def get_tasks():
    return tasks


# POST /tasks
@app.post("/tasks", status_code=201)
def create_task(task_data: dict):

    # Check if title exists
    if "title" not in task_data:
        return JSONResponse(
            status_code=400,
            content={"error": "title is required"}
        )

    # Get title
    title = task_data["title"]

    # Check if title is empty
    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "title cannot be empty"}
        )

    # Generate next ID
    new_id = max(task["id"] for task in tasks) + 1

    # Create new task
    new_task = {
        "id": new_id,
        "title": title,
        "done": False
    }

    # Add new task to the list
    tasks.append(new_task)

    # Return created task
    return new_task