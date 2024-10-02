from datetime import datetime

from fastapi import Body, Depends, FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import sign_jwt
from app.auth.models import UserSchema
from app.database import get_async_session
from app.schemas import TaskCreateOrUpdateSchema, TaskSchema

from .crud import create_task, delete_task, get_task, get_tasks, update_task

router = APIRouter()


# Получение списка задач
@router.get("/tasks/list", tags=["tasks"], response_model=list[TaskSchema])
async def get_tasks_list(
    db: AsyncSession = Depends(get_async_session),
) -> list[TaskSchema]:
    tasks = await get_tasks(db)
    return [TaskSchema.from_orm(task) for task in tasks]


# Создание задачи
@router.post("/tasks/create", tags=["tasks"], response_model=TaskSchema)
async def create_task_route(
    task: TaskCreateOrUpdateSchema, db: AsyncSession = Depends(get_async_session)
) -> TaskSchema:

    new_task = await create_task(db, task)
    return TaskSchema.from_orm(new_task)


# Получение конкретной задачи по ID
@router.get("/tasks/{task_id}", tags=["tasks"], response_model=TaskSchema)
async def get_single_task(
    task_id: int, db: AsyncSession = Depends(get_async_session)
) -> TaskSchema:
    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskSchema.from_orm(task)


# Обновление задачи
@router.patch(
    "/tasks/{task_id}/update",
    response_model=TaskSchema,
    dependencies=[Depends(JWTBearer())],
    tags=["tasks"],
)
async def update_task_route(
    task_id: int,
    task_update: TaskCreateOrUpdateSchema,
    db: AsyncSession = Depends(get_async_session),
) -> TaskSchema:
    updated_task = await update_task(db, task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskSchema.from_orm(updated_task)


# Удаление задачи
@router.delete("/tasks/{task_id}", tags=["tasks"], dependencies=[Depends(JWTBearer())])
async def delete_task_route(
    task_id: int, db: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    task_deleted = await delete_task(db, task_id)
    if not task_deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return JSONResponse(
        content={"message": "Task deleted successfully"}, status_code=200
    )


# Получение JWT токена
@router.post("/get_jwt", tags=["user"])
async def create_user(user: UserSchema = Body(...)) -> JSONResponse:
    return JSONResponse(content=sign_jwt(user.email), status_code=201)
