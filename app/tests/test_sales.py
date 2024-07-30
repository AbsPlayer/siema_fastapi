import json

from fastapi import status

from app import models
from app.database import SessionLocal
from .client import client

db = SessionLocal()
db_query = db.query(models.Sale)
product_id = db.query(models.Product).first().id

test_sale_data = {
    "quantity": 222,
    "created_at": "2024-07-20",
    "product_id": product_id,
}
wrong_test_sale_data = {
    "quantity": "1 piece",
    "created_at": "2024-07-20",
    "product_id": product_id,
}


def test_sales():
    first_row = db_query.first()
    sale_id = first_row.id

    response = client.get("/sales")
    assert response.status_code == status.HTTP_200_OK

    sales_count = db_query.count()
    resp = response.json()
    assert len(resp) == sales_count

    # test create sale
    sales_count = db_query.count()
    response = client.post(f"/sales", data=json.dumps(test_sale_data))
    test_sale_id = response.json()["id"]
    assert response.status_code == status.HTTP_200_OK
    assert db_query.count() == sales_count + 1

    # test create sale with wrong type value
    response = client.post(f"/sales", data=json.dumps(wrong_test_sale_data))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # test patch sale by id
    sales_count = db_query.count()
    sale_qty = db_query.filter_by(id=sale_id).first().quantity
    sale_created_at = db_query.filter_by(id=sale_id).first().created_at
    sale_product_id = db_query.filter_by(id=sale_id).first().product_id
    response = client.patch(
        f"/sale/{sale_id}",
        data=json.dumps(
            {
                "quantity": sale_qty + 100,
                "created_at": "2020-10-10",
                "product_id": sale_product_id,
            }
        ),
    )
    assert response.status_code == status.HTTP_200_OK
    assert db_query.count() == sales_count
    response = client.patch(
        f"/sale/{sale_id}",
        data=json.dumps(
            {
                "quantity": sale_qty - 100,  # return back quantity
                "created_at": sale_created_at.strftime("%Y-%m-%d"),  # and date
                "product_id": sale_product_id,
            }
        ),
    )
    assert response.status_code == status.HTTP_200_OK

    # test patch sale by id with wrong type value
    response = client.patch(f"/sale/{sale_id}", data=json.dumps(wrong_test_sale_data))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # test patch sale with wrong id
    response = client.patch("/sale/-999", data=json.dumps(test_sale_data))
    assert response.status_code == status.HTTP_200_OK

    # test delete sale by id
    response = client.delete(f"/sale/{test_sale_id}")
    assert response.status_code == status.HTTP_200_OK

    # test delete sale with wrong id
    response = client.delete("/sale/-999")
    assert response.status_code == status.HTTP_200_OK
