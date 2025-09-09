from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database
from app.models import product as models, shop as shop_models, user as user_models
from app.schemas import product as schemas
from app.routes.auth import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Add product to shop
@router.post("/add/{shop_id}", response_model=schemas.ProductResponse)
def create_product(shop_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: user_models.User = Depends(get_current_user)):
    shop = db.query(shop_models.Shop).filter(shop_models.Shop.id == shop_id, shop_models.Shop.owner_id == current_user.id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found or not yours")

    db_product = models.Product(**product.dict(), shop_id=shop_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# 2. View all products in my shops
@router.get("/mine", response_model=list[schemas.ProductResponse])
def get_my_products(db: Session = Depends(get_db), current_user: user_models.User = Depends(get_current_user)):
    shops = db.query(shop_models.Shop).filter(shop_models.Shop.owner_id == current_user.id).all()
    shop_ids = [shop.id for shop in shops]
    return db.query(models.Product).filter(models.Product.shop_id.in_(shop_ids)).all()
