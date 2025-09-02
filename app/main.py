from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app import database
from app.models import user, shop
from app.routes import user as user_routes, shop as shop_routes

# Create database tables
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Include routers
app.include_router(user_routes.router)
app.include_router(shop_routes.router)

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve registration and login pages
@app.get("/register")
def register_page():
    return FileResponse("static/register.html")

@app.get("/login")
def login_page():
    return FileResponse("static/login.html")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Shopping Mall API is running 🚀"}
