import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")

engine = create_engine(DATABASE_URL)


def initialize_database():
    with engine.begin() as connection:

        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN DEFAULT FALSE
            )
        """))

        result = connection.execute(
            text("SELECT COUNT(*) FROM tasks")
        )

        count = result.scalar()

        if count == 0:
            connection.execute(text("""
                INSERT INTO tasks (title, done)
                VALUES
                    ('Learn FastAPI', FALSE),
                    ('Learn PostgreSQL', FALSE),
                    ('Build CRUD API', FALSE)
            """))
def get_all_tasks():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM tasks ORDER BY id")
        )
        return [dict(row._mapping) for row in result]


def get_task_by_id(task_id):
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM tasks WHERE id = :id"),
            {"id": task_id}
        )
        row = result.fetchone()

        if row:
            return dict(row._mapping)

        return None


def create_task(title, done=False):
    with engine.begin() as connection:
        result = connection.execute(
            text("""
                INSERT INTO tasks (title, done)
                VALUES (:title, :done)
                RETURNING id, title, done
            """),
            {
                "title": title,
                "done": done
            }
        )

        row = result.fetchone()

        if row is None:
            return None

        return dict(row._mapping)

def update_task(task_id, title, done):
    with engine.begin() as connection:
        result = connection.execute(
            text("""
                UPDATE tasks
                SET title = :title, done = :done
                WHERE id = :id
                RETURNING id, title, done
            """),
            {
                "id": task_id,
                "title": title,
                "done": done
            }
        )

        row = result.fetchone()

        if row is None:
            return None

        return dict(row._mapping)

def delete_task(task_id):
    with engine.begin() as connection:
        result = connection.execute(
            text("""
                DELETE FROM tasks
                WHERE id = :id
                RETURNING id, title, done
            """),
            {"id": task_id}
        )

        row = result.fetchone()

        if row is None:
            return None

        return dict(row._mapping)