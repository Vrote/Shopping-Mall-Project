from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database
from app.models.shop import Shop
from app.schemas.shop import ShopCreate, ShopOut

router = APIRouter(prefix="/shops", tags=["Shops"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ShopOut)
def create_shop(shop: ShopCreate, db: Session = Depends(get_db)):
    db_shop = Shop(**shop.dict())
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop

@router.get("/", response_model=list[ShopOut])
def list_shops(db: Session = Depends(get_db)):
    return db.query(Shop).all()
