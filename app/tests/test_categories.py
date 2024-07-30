import json

from fastapi import status

from app import models
from app.database import SessionLocal
from .client import client

db = SessionLocal()
db_query = db.query(models.Category)

test_category_data = {"name": "TEST category"}
wrong_test_category_data = {"name": 1234567890}


def test_categories():
    response = client.get("/categories")
    assert response.status_code == status.HTTP_200_OK

    categories_count = db_query.count()
    resp = response.json()
    assert len(resp) == categories_count


def test_category():
    first_row = db_query.first()
    category_id = first_row.id

    # test get category by id
    response = client.get(f"/category/{category_id}")
    assert response.status_code == status.HTTP_200_OK
    resp = response.json()
    assert resp["name"] == first_row.name

    # test get non exist category by id
    response = client.get("/category/-999")
    assert response.status_code == status.HTTP_200_OK

    # test create category
    categories_count = db_query.count()
    response = client.post(f"/categories", data=json.dumps(test_category_data))
    assert response.status_code == status.HTTP_200_OK
    assert db_query.count() == categories_count + 1

    # test create category with wrong type value
    response = client.post(f"/categories", data=json.dumps(wrong_test_category_data))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # test patch category by id
    categories_count = db_query.count()
    category_name = db_query.filter_by(id=category_id).first().name
    response = client.patch(
        f"/category/{category_id}",
        data=json.dumps({"name": f"{category_name} (changed)"}),
    )
    assert response.status_code == status.HTTP_200_OK
    assert db_query.count() == categories_count
    response = client.patch(
        f"/category/{category_id}",
        data=json.dumps({"name": f"{category_name}"}),  # return back previous name
    )
    assert response.status_code == status.HTTP_200_OK

    # test patch category by id with wrong type value
    response = client.patch(
        f"/category/{category_id}", data=json.dumps(wrong_test_category_data)
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # test patch category with wrong id
    response = client.patch("/category/-999", data=json.dumps(test_category_data))
    assert response.status_code == status.HTTP_200_OK

    # test delete category by id
    test_category_id = db_query.filter_by(name=test_category_data["name"]).first().id
    response = client.delete(f"/category/{test_category_id}")
    assert response.status_code == status.HTTP_200_OK

    # test delete category with wrong id
    response = client.delete("/category/-999")
    assert response.status_code == status.HTTP_200_OK

    # test getting all products in category
    response = client.get(f"/category/{category_id}/products")
    product_count = len(models.Category.read_by_id(db, category_id).products)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == product_count

    # test getting all sales in category
    response = client.get(f"/category/{category_id}/sales")
    sales_count = len(
        [
            product.sales
            for product in models.Category.read_by_id(db, category_id).products
            if product.sales
        ]
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == sales_count
