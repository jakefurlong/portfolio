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
