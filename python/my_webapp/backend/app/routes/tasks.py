from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Task as TaskModel
from app.schemas.task import Task as TaskSchema

router = APIRouter()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to create a task
@router.post("/tasks/")
def create_task(task: TaskSchema, db: Session = Depends(get_db)):
    # Check for duplicate title
    existing_task = db.query(TaskModel).filter(TaskModel.title == task.title).first()
    if existing_task:
        raise HTTPException(status_code=400, detail="Task title already exists")
    
    new_task = TaskModel(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task added successfully", "task": new_task}

# Route to get all tasks with optional filtering by completion status and pagination
@router.get("/tasks/")
def get_all_tasks(
    completed: bool = Query(None, description="Filter tasks by completion status"),
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(10, gt=0, le=100, description="Max number of tasks to return"),
    db: Session = Depends(get_db)
):
    """
    Get all tasks with optional filters:
    - completed: Filter tasks based on completion status.
    - skip: Offset for pagination.
    - limit: Limit the number of tasks returned (default 10, max 100).
    - Sorted by 'day' in ascending order.
    """
    query = db.query(TaskModel)

    if completed is not None:
        query = query.filter(TaskModel.completed == completed)

    # Apply default sorting by day
    query = query.order_by(asc(TaskModel.day))

    # Apply pagination
    tasks = query.offset(skip).limit(limit).all()
    total_tasks = query.count()

    return {
        "total_tasks": total_tasks,
        "page_size": len(tasks),
        "tasks": tasks
    }

# Route to get tasks by day
@router.get("/tasks/{day}")
def get_tasks_by_day(day: str, db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).filter(TaskModel.day.ilike(day)).all()
    return {"tasks": tasks}

# Route to mark a task as complete
@router.put("/tasks/{title}/complete")
def mark_task_complete(title: str, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.title == title).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = True
    db.commit()
    return {"message": f"Task '{title}' marked as complete", "task": task}

# Route to update a task
@router.put("/tasks/{title}")
def update_task(title: str, updated_task: TaskSchema, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.title == title).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Ensure no other task has the updated title
    if updated_task.title.lower() != title.lower():
        duplicate_task = db.query(TaskModel).filter(TaskModel.title == updated_task.title).first()
        if duplicate_task:
            raise HTTPException(status_code=400, detail="Task title already exists")

    # Update task fields
    task.title = updated_task.title
    task.description = updated_task.description
    task.day = updated_task.day
    task.completed = updated_task.completed
    db.commit()
    db.refresh(task)
    return {"message": f"Task '{title}' updated successfully", "task": task}

# Route to delete a task
@router.delete("/tasks/{title}")
def delete_task(title: str, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.title == title).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": f"Task '{title}' deleted successfully"}
