from faker import Faker
from fastapi import HTTPException

from app.database import SessionLocal
from app.models import Category, Product, Sale

QTY_CATEGORIES = 10
QTY_PRODUCTS = 100
QTY_SALES = 1000

fake = Faker()
db = SessionLocal()

# if it needs to raise exception during DELETE or PATCH some item - change to `True`
# otherwise wrong request will return 'None' (Null)
RAISE_EXCEPTION = False


def fill_categories(qty: int = QTY_CATEGORIES):
    for _ in range(qty):
        category = Category()
        category.name = fake.company()
        category.save(db)


def fill_products(qty: int = QTY_PRODUCTS):
    for _ in range(qty):
        product = Product()
        categories = Category.read(db)
        product.name = f"{fake.suffix()} {fake.name()}"
        product.price = fake.pyfloat(
            right_digits=2, positive=True, min_value=1, max_value=10000
        )
        product.category_id = fake.random_element(categories).id
        product.save(db)


def fill_sales(qty: int = QTY_SALES):
    for _ in range(qty):
        sale = Sale()
        products = Product.read(db)
        sale.quantity = fake.pyint(min_value=1, max_value=1000)
        sale.created_at = fake.date_time_between(start_date="-180d")
        sale.product_id = fake.random_element(products).id
        sale.save(db)


def fill_fake_data(
    qty_categories: int = QTY_CATEGORIES,
    qty_products: int = QTY_PRODUCTS,
    qty_sales: int = QTY_SALES,
):
    fill_categories(qty_categories)
    fill_products(qty_products)
    fill_sales(qty_sales)

    db.close()


def raise_exception(do_exc=RAISE_EXCEPTION):
    if do_exc:
        raise HTTPException(status_code=404, detail="Item not found")
    return
