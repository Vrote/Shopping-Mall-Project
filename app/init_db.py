# app/init_db.py
print("init_db.py started...")

from app.database import Base, engine
from app.models import user

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
