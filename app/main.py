from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, crud
from .database import engine, get_db


app = FastAPI()

def init_db():
    """Создает таблицы в базе данных, если они не существуют."""
    models.Base.metadata.create_all(bind=engine)

# Вызов функции инициализации базы данных
init_db()

@app.post("/products/")
def create_product(name: str, price: int, category_id: int, db: Session = Depends(get_db)):
    product = models.Product(name=name, price=price, category_id=category_id)
    return crud.create_product(db=db, product=product)

@app.get("/products/{product_id}")
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/")
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit)

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.delete_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}


@app.post("/categories/")
def create_category(name: str, db: Session = Depends(get_db)):
    category = models.Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
