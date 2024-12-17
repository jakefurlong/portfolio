# Project Documentation - My WebApp

## Getting Started with FastAPI

Create virtual env in backend directory.

 ```
 pip install fastapi uvicorn
 ```

Create main.py in app directory. Write initial code.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
```

Make sure you're in the main directory.

Go to localhost:8000 and you should see the hello world message. Next, try to go ot localhost:8000/docs and you should see the FastAPI documentation that is automatically generated with Swagger UI. Swagger UI is an interactive documentation tool automatically provided by Fast API. It helps you visualize, test, and understand your API without writing any extra code. It provides interactive API documentation, an API testing tool, and helps developers understand your API.

You can also visit [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) as another documentation option. Some may prefer the visual asthetic. 

It's probably also worth showing how to do this in Postman.

Next, add the following code to `main.py` to add a dynamic route and query parameters.

```python
# Dynamic route with path and query parameters
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    """
    Path parameter: item_id (int)
    Query parameter: q (optional string)
    """
    return {"item_id": item_id, "query_param": q}
```

Reload the app `uvicorn main:app --reload`. After the page loads, trying going to `localhost:8000/items/42` and `http://127.0.0.1:8000/items/42?q=test`.

Once you've tested that it's time to update the code again and create a POST endpoint.

Add to main.py
```python
from pydantic import BaseModel

# Pydantic model to validate input data
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    in_stock: bool

# POST route to create a new item
@app.post("/items/")
def create_item(item: Item):
    return {"message": "Item created successfully", "item": item}
```

Pydantic validates the request body to ensure correct input and the POST route receives the `item` object and echoes it back. REload the app and open the Swagger UI. 
```
uvicorn main:app --reload
```
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Expand the POST /items/ arrow and click "Try it out." Then enter some test data in the Request body section:

```json
{
  "name": "Laptop",
  "description": "A high-performance laptop",
  "price": 999.99,
  "in_stock": true
}
```
Click "Execute." You're looking for a 200 OK return value with the message "Item created successfully."

We have a couple routes now so it's time to restructure our directory. 

```
my_webapp/
│
├── app/
│   ├── __init__.py
│   ├── main.py           # Entry point
│   ├── routes/           # API routes
│   │   ├── __init__.py
│   │   ├── items.py      # Item-related routes
│   └── schemas/          # Pydantic schemas
│       ├── __init__.py
│       ├── item.py
├── requirements.txt      # Dependencies
└── README.md
```
I am using `README.md` to write myself instructions on how to create this application.

Move code to folders:
- Routes    --> routes/items.py
- Schemas   --> schemas/item.py

Examples:
```python
# app/routes/items.py
from fastapi import APIRouter
from app.schemas.item import Item

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@router.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query_param": q}

@router.post("/items/")
def create_item(item: Item):
    return {"message": "Item created successfully", "item": item}
```
```python
# app/schemas/item.py
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    in_stock: bool
```

Then update `main.py` to use the router:

```python
from fastapi import FastAPI
from app.routes import items  # Import the items router

app = FastAPI()

# Include the router
app.include_router(items.router)

# Root route (optional, can be moved too)
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```

Now, all the routes related to "items" are in their own file, all input/output data validation (Pydantic models) is in a dedicated file, and main.py acts as the central entry point, bringing everythingtogether with `include_router`.

Reload the app and try to test again.

Success!

Now that the app is working with the new structure, it's time to add some context to our app and decide what it's going to do. I decided to make a checklist app that has a unique checklist for each day of the week. I will use it to train myself on Kubernetes during my daily workout.

## Checklist App

1. Define the data model
2. Add routes
3. Include the Router in main.py
4. Test

### Define the data model

replace app/schemas/item.py with app/schemas/task.py

```python
from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    day: str  # e.g., "Monday", "Tuesday"
    completed: bool = False
```

### Add routes

```python
from fastapi import APIRouter
from app.schemas.task import Task

router = APIRouter()

# In-memory list to store tasks
tasks = []

# Route to create a task
@router.post("/tasks/")
def create_task(task: Task):
    tasks.append(task.dict())
    return {"message": "Task added successfully", "task": task}

# Route to get tasks for a specific day
@router.get("/tasks/{day}")
def get_tasks(day: str):
    filtered_tasks = [task for task in tasks if task["day"].lower() == day.lower()]
    return {"tasks": filtered_tasks}

# Route to get all tasks
@router.get("/tasks/")
def get_all_tasks():
    return {"tasks": tasks}
```

### Include the Router in main.py

```python
from fastapi import FastAPI
from app.routes import tasks

app = FastAPI()

# Include the tasks router
app.include_router(tasks.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Daily Checklist App!"}
```

### Test

Open Swagger UI and make a POST request. Then, get all tasks with a GET request and confirm the task was added successfuly. You should also see this message in the POST output but we want to double-check. Lastly, check the specific day to make sure you can return a single task.

## Add a route to mark tasks complete

In app/routes/tasks.py add a PUT route:

```python
from fastapi import APIRouter, HTTPException
from app.schemas.task import Task

router = APIRouter()

# In-memory list to store tasks
tasks = []

# Route to create a task
@router.post("/tasks/")
def create_task(task: Task):
    tasks.append(task.dict())
    return {"message": "Task added successfully", "task": task}

# Route to get tasks for a specific day
@router.get("/tasks/{day}")
def get_tasks(day: str):
    filtered_tasks = [task for task in tasks if task["day"].lower() == day.lower()]
    return {"tasks": filtered_tasks}

# Route to get all tasks
@router.get("/tasks/")
def get_all_tasks():
    return {"tasks": tasks}

# Route to mark a task as complete
@router.put("/tasks/{title}")
def mark_task_complete(title: str):
    for task in tasks:
        if task["title"].lower() == title.lower():
            task["completed"] = True
            return {"message": f"Task '{title}' marked as complete", "task": task}
    raise HTTPException(status_code=404, detail=f"Task '{title}' not found")
```
The PUT route tasks the task title as a path parameter and loops through the tasks, finds the matching title, and updates the completed field to True. If no task matches the given title, it raises a 404 error. 

Let's do a test. Run the app, and test the endpoints in Swagger. Add a new task, mark the task as complete. Verify that the task now has a `"completed: true"`.

## Add the delete route to delete tasks

In app/routes/tasks.py, add a DELETE route to remove a task based on its title.

```python
from fastapi import APIRouter, HTTPException
from app.schemas.task import Task

router = APIRouter()

# In-memory list to store tasks
tasks = []

# Route to create a task
@router.post("/tasks/")
def create_task(task: Task):
    tasks.append(task.dict())
    return {"message": "Task added successfully", "task": task}

# Route to get tasks for a specific day
@router.get("/tasks/{day}")
def get_tasks(day: str):
    filtered_tasks = [task for task in tasks if task["day"].lower() == day.lower()]
    return {"tasks": filtered_tasks}

# Route to get all tasks
@router.get("/tasks/")
def get_all_tasks():
    return {"tasks": tasks}

# Route to mark a task as complete
@router.put("/tasks/{title}")
def mark_task_complete(title: str):
    for task in tasks:
        if task["title"].lower() == title.lower():
            task["completed"] = True
            return {"message": f"Task '{title}' marked as complete", "task": task}
    raise HTTPException(status_code=404, detail=f"Task '{title}' not found")

# Route to delete a task by title
@router.delete("/tasks/{title}")
def delete_task(title: str):
    for index, task in enumerate(tasks):
        if task["title"].lower() == title.lower():
            deleted_task = tasks.pop(index)
            return {"message": f"Task '{title}' deleted successfully", "task": deleted_task}
    raise HTTPException(status_code=404, detail=f"Task '{title}' not found")

```
Test that you can delete a task in the Swagger UI. You should know how to go through the steps by now, if not scroll up. Perform test in Postman as well.

## Add a route to update tasks with a PUT route

```python
from fastapi import APIRouter, HTTPException
from app.schemas.task import Task
from typing import Optional

router = APIRouter()

# In-memory list to store tasks
tasks = []

# Route to create a task
@router.post("/tasks/")
def create_task(task: Task):
    tasks.append(task.dict())
    return {"message": "Task added successfully", "task": task}

# Route to get tasks for a specific day
@router.get("/tasks/{day}")
def get_tasks(day: str):
    filtered_tasks = [task for task in tasks if task["day"].lower() == day.lower()]
    return {"tasks": filtered_tasks}

# Route to get all tasks
@router.get("/tasks/")
def get_all_tasks():
    return {"tasks": tasks}

# Route to mark a task as complete
@router.put("/tasks/{title}/complete")
def mark_task_complete(title: str):
    for task in tasks:
        if task["title"].lower() == title.lower():
            task["completed"] = True
            return {"message": f"Task '{title}' marked as complete", "task": task}
    raise HTTPException(status_code=404, detail=f"Task '{title}' not found")

# Route to delete a task by title
@router.delete("/tasks/{title}")
def delete_task(title: str):
    for index, task in enumerate(tasks):
        if task["title"].lower() == title.lower():
            deleted_task = tasks.pop(index)
            return {"message": f"Task '{title}' deleted successfully", "task": deleted_task}
    raise HTTPException(status_code=404, detail=f"Task '{title}' not found")

# Route to update a task
@router.put("/tasks/{title}")
def update_task(title: str, updated_task: Task):
    for index, task in enumerate(tasks):
        if task["title"].lower() == title.lower():
            tasks[index] = updated_task.dict()
            return {"message": f"Task '{title}' updated successfully", "task": updated_task}
    raise HTTPException(status_code=404, detail=f"Task '{title}' not found")
```

## Add routes for data validation to ensure there are no duplicates




```python

# add to app/routes/tasks.py (replace)

# Route to create a task
@router.post("/tasks/")
def create_task(task: Task):
    # Check for duplicate title
    for existing_task in tasks:
        if existing_task["title"].lower() == task.title.lower():
            raise HTTPException(
                status_code=400,
                detail=f"Task with title '{task.title}' already exists."
            )
    tasks.append(task.dict())
    return {"message": "Task added successfully", "task": task}

# Route to update a task
@router.put("/tasks/{title}")
def update_task(title: str, updated_task: Task):
    # Ensure the task exists
    for index, task in enumerate(tasks):
        if task["title"].lower() == title.lower():
            # Validate no duplicate title (except for the current task)
            for existing_task in tasks:
                if (
                    existing_task["title"].lower() == updated_task.title.lower()
                    and existing_task != task
                ):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Task with title '{updated_task.title}' already exists."
                    )
            # Update the task
            tasks[index] = updated_task.dict()
            return {"message": f"Task '{title}' updated successfully", "task": updated_task}
    raise HTTPException(status_code=404, detail=f"Task '{title}' not found")
```

## Add optional status completion filter

```python
@router.get("/tasks/")
def get_all_tasks(completed: bool = Query(None, description="Filter tasks by completion status")):
    if completed is None:
        return {"tasks": tasks}
    filtered_tasks = [task for task in tasks if task["completed"] == completed]
    return {"tasks": filtered_tasks}
```

Also, add `from fastapi import APIRouter, HTTPException, Query` to the import section at the top of the page.

## Now it's time for a DB!

Install stuff

`pip install sqlalchemy psycopg2-binary pydantic`

Create the database using docker-compose...

```
services:
  postgres:
    image: postgres:latest
    container_name: postgres_db
    restart: always
    environment:
      POSTGRES_DB: taskdb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: Delor3an
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```
Next, define the task model. Create `db/models.py`.

```python
from sqlalchemy import Column, Integer, String, Boolean
from app.db.session import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    day = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
```
In here, the table name is tasks, and each task has an id, title, description, day, and completed status.

Then, create the database tables. Here's a script you can run (or do it in pgadmin).

```python
from app.db.session import engine, Base
from app.db.models import Task

# Create all tables
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")
```
Then run the script (from the parent directory of app)
```python
python3 create_db.py
```
Note: if you don't use python 3 it won't be able to find the packages.

## Modify your routes/tasks.py to interact with the database

```python
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

# Route to get all tasks with optional filtering by completion status
@router.get("/tasks/")
def get_all_tasks(completed: bool = Query(None, description="Filter tasks by completion status"), db: Session = Depends(get_db)):
    query = db.query(TaskModel)
    if completed is not None:
        query = query.filter(TaskModel.completed == completed)
    tasks = query.all()
    return {"tasks": tasks}

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

```

## Update your main app entry point to include the database-powered routes

```python
from fastapi import FastAPI
from app.routes import tasks

app = FastAPI()

# Include the tasks router
app.include_router(tasks.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Daily Checklist App!"}

```

## Test!

`uvicorn app.main:app --reload`

Test using Swagger UI:
- POST /tasks/: Add a new task.
- GET /tasks/?completed=false: Fetch incomplete tasks.
- PUT /tasks/{title}/complete: Mark a task as complete.
- DELETE /tasks/{title}: Delete a task.

## Add pagination for large task lists

Update the primary GET route to include a skip for the number of tasks to skip and a limit for a maximum number of tasks to return.

```python
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
    """
    query = db.query(TaskModel)
    if completed is not None:
        query = query.filter(TaskModel.completed == completed)

    # Apply pagination
    tasks = query.offset(skip).limit(limit).all()
    total_tasks = query.count()

    return {
        "total_tasks": total_tasks,
        "page_size": len(tasks),
        "tasks": tasks
    }
```

# Add default sorting by day

Add `from sqlalchemy import asc`

Update primary GET route.

```python
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
```

## containerize app

Create a Dockerfile for the api app

```
# Use the official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port
EXPOSE 8000

# Start the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

```

## Update the database connection

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Read the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Delor3an@db:5432/taskdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

```

Create the docker-compose file:

```
services:
  api:
    build: .
    container_name: fastapi_app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://postgres:Delor3an@db:5432/taskdb

  db:
    image: postgres:latest
    container_name: postgres_db
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: Delor3an
      POSTGRES_DB: taskdb
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:

```

Update requirements file:

```text
fastapi
uvicorn
sqlalchemy
psycopg2-binary
pydantic
```
Update main file to create the DB tasks table (reads from models.py)

```python
from fastapi import FastAPI
from app.routes import tasks
from app.db.session import engine
from app.db.models import Base

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the tasks router
app.include_router(tasks.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Daily Checklist App!"}

```

Build the containers...

`docker-compose build`

Restart the containers...

`docker-compose up`

Create a DB in pgadmin to review changes and use the Swagger UI to perform tests.