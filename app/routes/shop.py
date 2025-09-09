from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database
from app.models import shop as models, user as user_models
from app.schemas import shop as schemas
from app.routes.user import get_current_user   # ✅ import function

router = APIRouter(prefix="/shops", tags=["Shops"])

# DB dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Add new shop
@router.post("/add", response_model=schemas.ShopResponse)
def create_shop(
    shop: schemas.ShopCreate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    if current_user.role != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can add shops")
    db_shop = models.Shop(**shop.dict(), owner_id=current_user.id)
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop

# 2. View seller’s own shops
@router.get("/mine", response_model=list[schemas.ShopResponse])
def get_my_shops(
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    if current_user.role != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can view their shops")
    return db.query(models.Shop).filter(models.Shop.owner_id == current_user.id).all()

# 3. Update shop
@router.put("/{shop_id}", response_model=schemas.ShopResponse)
def update_shop(
    shop_id: int,
    shop_update: schemas.ShopUpdate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    db_shop = db.query(models.Shop).filter(models.Shop.id == shop_id, models.Shop.owner_id == current_user.id).first()
    if not db_shop:
        raise HTTPException(status_code=404, detail="Shop not found or not yours")

    if shop_update.name:
        db_shop.name = shop_update.name
    if shop_update.location:
        db_shop.location = shop_update.location

    db.commit()
    db.refresh(db_shop)
    return db_shop

# 4. Delete shop
@router.delete("/{shop_id}")
def delete_shop(
    shop_id: int,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    db_shop = db.query(models.Shop).filter(models.Shop.id == shop_id, models.Shop.owner_id == current_user.id).first()
    if not db_shop:
        raise HTTPException(status_code=404, detail="Shop not found or not yours")

    db.delete(db_shop)
    db.commit()
    return {"message": "Shop deleted successfully"}
