
from fastapi import APIRouter, HTTPException

from schemas.task import TaskCreate, TaskPut, TaskPatch
from crud.tasks import (
    create_task_record,
    get_all_task_records,
    get_user_task_records,
    get_task_record,
    replace_task_record,
    patch_task_record,
    delete_task_record,
)
from crud.users import get_user_record


router = APIRouter(tags=["Tasks"])


@router.post("/users/{user_id}/tasks", status_code=201)
def create_task(user_id: int, task_data: TaskCreate):
    try:
        user = get_user_record(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        task = create_task_record(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
        )

        return {
            "message": "Task created successfully",
            "task": task,
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Could not create task")


@router.get("/tasks")
def get_all_tasks():
    try:
        return get_all_task_records()
    except Exception:
        raise HTTPException(status_code=500, detail="Could not retrieve tasks")


@router.get("/users/{user_id}/tasks")
def get_user_tasks(user_id: int):
    try:
        user = get_user_record(user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return get_user_task_records(user_id)

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Could not retrieve user tasks")


@router.get("/users/{user_id}/tasks/{task_id}")
def get_task(user_id: int, task_id: int):
    try:
        task = get_task_record(user_id, task_id)

        if task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found for this user",
            )

        return task

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Could not retrieve task")


@router.put("/users/{user_id}/tasks/{task_id}")
def replace_task(user_id: int, task_id: int, task_data: TaskPut):
    try:
        task = replace_task_record(
            user_id=user_id,
            task_id=task_id,
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
        )

        if task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found for this user",
            )

        return {
            "message": "Task replaced successfully",
            "task": task,
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Could not replace task")


@router.patch("/users/{user_id}/tasks/{task_id}")
def patch_task(user_id: int, task_id: int, task_data: TaskPatch):
    try:
        updates = task_data.model_dump(exclude_unset=True)

        task = patch_task_record(
            user_id=user_id,
            task_id=task_id,
            updates=updates,
        )

        if task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found for this user",
            )

        return {
            "message": "Task updated successfully",
            "task": task,
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Could not update task")


@router.delete("/users/{user_id}/tasks/{task_id}")
def delete_task(user_id: int, task_id: int):
    try:
        task = delete_task_record(user_id, task_id)

        if task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found for this user",
            )

        return {
            "message": "Task deleted successfully",
            "task": task,
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Could not delete task")
