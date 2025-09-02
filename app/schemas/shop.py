from pydantic import BaseModel

class ShopCreate(BaseModel):
    name: str
    category: str
    location: str | None = None

class ShopOut(BaseModel):
    id: int
    name: str
    category: str
    location: str | None = None

    class Config:
        orm_mode = True
