from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database
from app.models import product as models, shop as shop_models, user as user_models
from app.schemas import product as schemas
from app.routes.auth import get_current_user  # Ensure no circular import

router = APIRouter(prefix="/products", tags=["Products"])

# Database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Add product
@router.post("/add/{shop_id}", response_model=schemas.ProductResponse)
def create_product(
    shop_id: int,
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    shop = db.query(shop_models.Shop).filter(
        shop_models.Shop.id == shop_id,
        shop_models.Shop.owner_id == current_user.id
    ).first()

    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found or not yours")

    db_product = models.Product(**product.dict(), shop_id=shop_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# Get products for a shop
@router.get("/{shop_id}", response_model=list[schemas.ProductResponse])
def get_products(
    shop_id: int,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    shop = db.query(shop_models.Shop).filter(
        shop_models.Shop.id == shop_id,
        shop_models.Shop.owner_id == current_user.id
    ).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found or not yours")

    return db.query(models.Product).filter(models.Product.shop_id == shop_id).all()


# Update product
@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int,
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    db_product = db.query(models.Product).join(shop_models.Shop).filter(
        models.Product.id == product_id,
        shop_models.Shop.owner_id == current_user.id
    ).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found or not yours")

    db_product.name = product.name
    db_product.price = product.price
    db_product.description = getattr(product, "description", None)
    db.commit()
    db.refresh(db_product)
    return db_product


# Delete product
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    db_product = db.query(models.Product).join(shop_models.Shop).filter(
        models.Product.id == product_id,
        shop_models.Shop.owner_id == current_user.id
    ).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found or not yours")

    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted"}
