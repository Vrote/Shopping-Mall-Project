from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import database
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
import re

# ---------------- JWT Settings ----------------
SECRET_KEY = "your_super_secret_key_here"  # Replace with a secure secret in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ---------------- Password Context ----------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/users", tags=["Users"])

# ---------------- Database Dependency ----------------
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Register User ----------------
@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    db_user = db.query(User).filter(User.email == user.email.lower()).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_password = pwd_context.hash(user.password)

    # Create user object
    new_user = User(
        name=user.name.title(),
        email=user.email.lower(),
        hashed_password=hashed_password,
        role="customer"  # fixed role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ---------------- Login Request Model ----------------
class LoginRequest(BaseModel):
    email: str
    password: str

# ---------------- Login User ----------------
@router.post("/login")
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    # Get user by email
    user = db.query(User).filter(User.email == data.email.lower()).first()
    
    # Check user exists and password matches
    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": user.email, "exp": datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": user.id, "name": user.name, "email": user.email}
    }

# ---------------- Get User by ID ----------------
@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
