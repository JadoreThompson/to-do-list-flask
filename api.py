import hashlib

import psycopg2
from psycopg2 import sql
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import models
import datetime

app = FastAPI()


class User(BaseModel):
    username: str
    email: str
    password: str


class LoginUser(BaseModel):
    email: str
    password: str


class Task(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: str


class UpdateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None


user_db = {
    1: User(username="user1", email="user1@email.com", password="password1"),
    2: User(username="user2", email="user2@email.com", password="password2"),
}

task_db = {
    1: Task(title="Task 1", description="Description 1", due_date="2021-09-01"),
    2: Task(title="Task 2", description="Description 2", due_date="2021-09-02"),
    3: Task(title="Task 3", description="Description 3", due_date="2021-09-03"),
}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/tasks/{user_id}", response_model=List[Task])
def get_all_tasks(user_id: int, task_title: Optional[str] = None, task_due_date: Optional[str] = None):
    with psycopg2.connect(**models.conn_params) as conn:
        with conn.cursor() as cur:
            if task_title is not None:
                db_query = sql.SQL("""
                    SELECT * FROM tasks
                    WHERE title = %s;
                """)
                cur.execute(db_query, task_title, )
                rows = cur.fetchall()
                for row in rows:
                    task = [Task(title=row[1], description=row[2], due_date=row[3].isoformat())]

                return task

            if task_due_date is not None:
                db_query = sql.SQL("""
                    SELECT * FROM tasks
                    WHERE due_date = %s;
                """)
                cur.execute(db_query, task_due_date, )
                rows = cur.fetchall()
                for row in rows:
                    task = [Task(title=row[1], description=row[2], due_date=row[3].isoformat())]

                return task

            db_query = sql.SQL("""
                SELECT * FROM tasks
                WHERE user_id = %s;
            """)
            cur.execute(db_query, str(user_id),)
            rows = cur.fetchall()
            for row in rows:
                task = [Task(title=row[1], description=row[2], due_date=row[3].isoformat())]

            return task




    # if task_title:
    #     return [task for task in task_db.values() if task.title == task_title]
    # if task_due_date:
    #     return [task for task in task_db.values() if task.due_date == task_due_date]
    #
    # return list(task_db.values())


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    with psycopg2.connect(**models.conn_params) as conn:
        with conn.cursor() as cur:
            db_query = sql.SQL("""
                SELECT * FROM tasks
                WHERE id = %s;
            """)
            cur.execute(db_query, str(task_id),)
            rows = cur.fetchall()
            for row in rows:
                task = [Task(title=row[1], description=row[2], due_date=row[3].isoformat())]

            return task


@app.post("/register")
def register(user: User):
    with psycopg2.connect(**models.conn_params) as conn:
        with conn.cursor() as cur:
            insert_script = sql.SQL("""
                INSERT INTO users (username, email, password)
                VALUES (%s, %s, %s)
                ON CONFLICT (email) DO NOTHING; 
            """)
            hashed_password = hashlib.md5(user.password.encode())
            cur.execute(insert_script, (user.username, user.email, str(hashed_password)),)

            return user


@app.post("/login", response_model=LoginUser)
def login(user: LoginUser):
    with psycopg2.connect(**models.conn_params) as conn:
        with conn.cursor() as cur:
            db_query = sql.SQL("""
                SELECT * FROM users
                WHERE email = %s;
            """)
            cur.execute(db_query, (user.email, ))
            rows = cur.fetchall()
            user = LoginUser(email=user.email, password=user.password)
            return user


@app.post("/tasks/create/{user_id}")
def create_task(user_id: int, task: Task):
    with psycopg2.connect(**models.conn_params) as conn:
        with conn.cursor() as cur:
            insert_script = sql.SQL("""
                INSERT INTO tasks (title, description, due_date, user_id)
                VALUES (%s, %s, %s, %s);
            """)
            cur.execute(insert_script, (task.title, task.description, task.due_date, user_id),)

            return task


@app.put("/tasks/update/{task_id}", response_model=Task)
def update_task(task_id: int, task: UpdateTask):
    if task_id not in task_db:
        raise HTTPException(status_code=404, detail="Task not found")

    with psycopg2.connect(**models.conn_params) as conn:
        with conn.cursor() as cur:
            db_query = sql.SQL("""
                SELECT * FROM tasks
                WHERE  id = %s;
            """)
            cur.execute(db_query, (task_id, ))
            rows = cur.fetchall()
            return rows

    existing_task = task_db[task_id]

    if task.title is not None:
        existing_task.title = task.title
    if task.description is not None:
        existing_task.description = task.description
    if task.due_date is not None:
        existing_task.due_date = task.due_date

    return existing_task


@app.delete("/tasks/delete/{task_id}")
def delete_task(task_id: int):
    if task_id not in task_db:
        raise HTTPException(status_code=404, detail="Task not found")

    del task_db[task_id]
    return {"message": "Task deleted successfully!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="127.0.0.1", port=8080, reload=True)
