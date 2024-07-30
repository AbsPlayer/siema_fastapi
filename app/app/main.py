from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app import models
from app.database import ModelBase, engine, get_database
from app.schemas import Category, Product, Sale
from app.utils import raise_exception

app = FastAPI()

ModelBase.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"ping": "pong"}


@app.get("/categories")
def read_categories(
    db: Session = Depends(get_database),
):
    return models.Category.read(db)


@app.post("/categories")
def create_category(category: Category, db: Session = Depends(get_database)):
    new_category = models.Category(**category.model_dump()).save(db)
    return new_category


@app.get("/category/{category_id}")
def read_category(
    category_id: int,
    db: Session = Depends(get_database),
):
    return models.Category.read_by_id(db, category_id)


@app.patch("/category/{category_id}")
def update_category(
    category_id: int,
    category: Category,
    db: Session = Depends(get_database),
):
    if models.Category.exists(db, category_id):
        upd_category = models.Category.read_by_id(db, category_id)

        for field in category.model_fields.keys():
            setattr(upd_category, field, getattr(category, field))

        return upd_category.save(db)
    return raise_exception()


@app.delete("/category/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_database)):
    if models.Category.exists(db, category_id):
        del_category = models.Category.read_by_id(db, category_id)
        del_category.destroy(db)
        return {"Success": f"Object destroyed (id={category_id})"}
    return raise_exception()


@app.get("/category/{category_id}/products")
def read_category_products(
    category_id: int,
    db: Session = Depends(get_database),
):
    return models.Category.read_by_id(db, category_id).products


@app.get("/category/{category_id}/sales")
def read_category_sales(
    category_id: int,
    db: Session = Depends(get_database),
):
    return [
        product.sales
        for product in models.Category.read_by_id(db, category_id).products
        if product.sales
    ]


@app.get("/products")
def read_products(
    db: Session = Depends(get_database),
):
    return models.Product.read(db)


@app.post("/products")
def create_product(product: Product, db: Session = Depends(get_database)):
    new_product = models.Product(**product.model_dump()).save(db)
    return new_product


@app.get("/product/{product_id}")
def read_product(
    product_id: int,
    db: Session = Depends(get_database),
):
    return models.Product.read_by_id(db, product_id)


@app.patch("/product/{product_id}")
def update_product(
    product_id: int,
    product: Product,
    db: Session = Depends(get_database),
):
    if models.Product.exists(db, product_id):
        upd_product = models.Product.read_by_id(db, product_id)

        for field in product.model_fields.keys():
            setattr(upd_product, field, getattr(product, field))

        return upd_product.save(db)
    return raise_exception()


@app.delete("/product/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_database)):
    if models.Product.exists(db, product_id):
        del_product = models.Product.read_by_id(db, product_id)
        del_product.destroy(db)
        return {"Success": f"Object destroyed (id={product_id})"}
    return raise_exception()


@app.get("/product/{product_id}/sales")
def read_product_sales(
    product_id: int,
    db: Session = Depends(get_database),
):
    return models.Product.read_by_id(db, product_id).sales


@app.get("/sales")
def read_sales(
    db: Session = Depends(get_database),
):
    return models.Sale.read(db)


@app.post("/sales")
def create_sale(sale: Sale, db: Session = Depends(get_database)):
    new_sale = models.Sale(**sale.model_dump()).save(db)
    return new_sale


@app.patch("/sale/{sale_id}")
def update_sale(
    sale_id: int,
    sale: Sale,
    db: Session = Depends(get_database),
):
    if models.Sale.exists(db, sale_id):
        upd_sale = models.Sale.read_by_id(db, sale_id)

        for field in sale.model_fields.keys():
            setattr(upd_sale, field, getattr(sale, field))

        return upd_sale.save(db)
    return raise_exception()


@app.delete("/sale/{sale_id}")
def delete_sale(sale_id: int, db: Session = Depends(get_database)):
    if models.Sale.exists(db, sale_id):
        del_sale = models.Sale.read_by_id(db, sale_id)
        del_sale.destroy(db)
        return {"Success": f"Object destroyed (id={sale_id})"}
    return raise_exception()
