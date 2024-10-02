from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_tasks(db: AsyncSession):
    result = await db.execute(select(models.Task))
    return result.scalars().all()


async def get_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(models.Task).filter(models.Task.id == task_id))
    return result.scalar_one_or_none()


async def create_task(db: AsyncSession, task: schemas.TaskCreateOrUpdateSchema):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def update_task(
    db: AsyncSession, task_id: int, task: schemas.TaskCreateOrUpdateSchema
):
    db_task = await get_task(db, task_id)
    if db_task:
        for key, value in task.dict(exclude_unset=True).items():
            setattr(db_task, key, value)
        await db.commit()
        await db.refresh(db_task)
        return db_task
    return None


async def delete_task(db: AsyncSession, task_id: int):
    db_task = await get_task(db, task_id)
    if db_task:
        await db.delete(db_task)
        await db.commit()
        return True
    return False
