from app.db.session import engine, Base
from app.db.models import Task

# Create all tables
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")
