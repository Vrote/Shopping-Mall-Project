# app/routes/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import database, models
from app.utils import decode_token  # your JWT decode function

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # login endpoint

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        user_id = decode_token(token)  # decode JWT to get user_id
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user
