from fastapi import FastAPI
from app import database
from app.models import user, shop
from app.routes import user as user_routes, shop as shop_routes

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(shop_routes.router)

@app.get("/")
def read_root():
    return {"message": "Shopping Mall API is running 🚀"}
