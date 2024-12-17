from sqlalchemy import Column, Integer, String, Boolean
from app.db.session import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    day = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
