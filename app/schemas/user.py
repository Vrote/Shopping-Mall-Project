from pydantic import BaseModel, EmailStr, validator
import re

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "customer"  # fixed role

    @validator('name')
    def name_must_have_first_last(cls, v):
        parts = v.strip().split()
        if len(parts) < 2:
            raise ValueError('Please enter both first name and last name')
        if not all(p.isalpha() for p in parts):
            raise ValueError('Name must contain only alphabets')
        return v.title()  # capitalize first letters

    @validator('email')
    def email_must_be_gmail(cls, v):
        if not v.endswith('@gmail.com'):
            raise ValueError('Email must be a valid @gmail.com address')
        return v.lower()

    @validator('password')
    def password_strong(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        orm_mode = True
