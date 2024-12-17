from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    day: str  # e.g., "Monday", "Tuesday"
    completed: bool = False