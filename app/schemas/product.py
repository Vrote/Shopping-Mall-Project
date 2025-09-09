from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: int
    description: str | None = None

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    description: str | None

    class Config:
        orm_mode = True
