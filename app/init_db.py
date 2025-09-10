# app/init_db.py
print("init_db.py started...")

from app.database import Base, engine
from app.models import user
from app.models import Shop
from app.models import Product


print("Creating database tables...")
Base.metadata.create_all(bind=engine)
