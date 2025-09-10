from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app import database
from app.models import user, shop
from app.routes import user as user_routes, shop as shop_routes, product as product_routes
import os

# Create database tables
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = ["*"]  # in production, replace with your frontend URL

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_routes.router)
app.include_router(shop_routes.router)
app.include_router(product_routes.router)

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve registration and login pages
@app.get("/register")
def register_page():
    return FileResponse("static/register.html")

@app.get("/login")
def login_page():
    return FileResponse("static/login.html")



@app.get("/dashboard")
def dashboard():
    return FileResponse(os.path.join("static", "dashboard.html"))


@app.get("/seller_products")
def seller_products_page():
    return FileResponse("static/seller_products.html")



# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Shopping Mall API is running 🚀"}
