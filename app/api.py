# app/api.py

from fastapi import FastAPI, Body, Depends
from app.models import TaskSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import sign_jwt
from app.auth.models import UserSchema, UserLoginSchema


app = FastAPI()

tasks = [
    {
        "id": 1,
        "created_at": "2024-09-30T12:30:00",
        "updated_at": "2024-10-01T09:15:00",
        "datetime_to_do": "2024-10-01T15:00:00",
        "task_info": "Завершить разработку API для To Do приложения.",
    }
]


users = []


@app.get("/tasks", tags=["tasks"])
async def get_tasks() -> dict:
    return {"data": tasks}


@app.post("/create_task", dependencies=[Depends(JWTBearer())], tags=["tasks"])
async def add_task(post: TaskSchema) -> dict:
    post.id = len(tasks) + 1
    tasks.append(post.dict())
    return {"data": "task added."}


@app.get("/task/{id}", tags=["tasks"])
async def get_single_task(id: int) -> dict:
    if id > len(tasks):
        return {"error": "No such post with the supplied ID."}

    for task in tasks:
        if task["id"] == id:
            return {"data": task}


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user)
    return sign_jwt(user.email)


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return sign_jwt(user.email)
    return {"error": "Wrong login details!"}
