import json

from fastapi import status

from app import models
from app.database import SessionLocal
from .client import client

db = SessionLocal()
db_query = db.query(models.Product)
category_id = db.query(models.Category).first().id

test_product_data = {
    "name": "TEST product",
    "price": 123.45,
    "category_id": category_id,
}
wrong_test_product_data = {
    "name": 123.45,
    "price": "TEST product",
    "category_id": category_id,
}


def test_products():
    response = client.get("/products")
    assert response.status_code == status.HTTP_200_OK

    products_count = db_query.count()
    resp = response.json()
    assert len(resp) == products_count


def test_product():
    first_row = db_query.first()
    product_id = first_row.id

    # test get product by id
    response = client.get(f"/product/{product_id}")
    assert response.status_code == status.HTTP_200_OK
    resp = response.json()
    assert resp["name"] == first_row.name
    assert resp["price"] == first_row.price

    # test get non exist product by id
    response = client.get("/product/-999")
    assert response.status_code == status.HTTP_200_OK

    # test create product
    products_count = db_query.count()
    response = client.post(f"/products", data=json.dumps(test_product_data))
    assert response.status_code == status.HTTP_200_OK
    assert db_query.count() == products_count + 1

    # test create product with wrong type value
    response = client.post(f"/products", data=json.dumps(wrong_test_product_data))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # test patch product by id
    products_count = db_query.count()
    product_name = db_query.filter_by(id=product_id).first().name
    product_price = db_query.filter_by(id=product_id).first().price
    product_category = db_query.filter_by(id=product_id).first().category_id
    response = client.patch(
        f"/product/{product_id}",
        data=json.dumps(
            {
                "name": f"{product_name} (changed)",
                "price": product_price + 1,
                "category_id": product_category,
            }
        ),
    )
    assert response.status_code == status.HTTP_200_OK
    assert db_query.count() == products_count
    response = client.patch(
        f"/product/{product_id}",
        data=json.dumps(
            {
                "name": f"{product_name}",  # return back previous name
                "price": product_price,  # and price
                "category_id": product_category,
            }
        ),
    )
    assert response.status_code == status.HTTP_200_OK

    # test patch product by id with wrong type value
    response = client.patch(
        f"/product/{product_id}", data=json.dumps(wrong_test_product_data)
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # test patch product with wrong id
    response = client.patch("/product/-999", data=json.dumps(test_product_data))
    assert response.status_code == status.HTTP_200_OK

    # test delete product by id
    test_product_id = db_query.filter_by(name=test_product_data["name"]).first().id
    response = client.delete(f"/product/{test_product_id}")
    assert response.status_code == status.HTTP_200_OK

    # test delete product with wrong id
    response = client.delete("/product/-999")
    assert response.status_code == status.HTTP_200_OK

    # test getting all sales of product
    response = client.get(f"/product/{product_id}/sales")
    sales_count = len(models.Product.read_by_id(db, product_id).sales)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == sales_count
