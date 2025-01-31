from sqlalchemy.orm import Session
from app.models.user_model import User, UserRole


def test_add_item_to_cart(client, setup_db, test_db_session: Session):
    client.post(
        "/register",
        json={"name": "John Doe", "email": "john@example.com", "password": "123456"},
    )

    admin_user = test_db_session.query(User).filter_by(email="john@example.com").first()
    admin_user.role = UserRole.ADMIN.value
    test_db_session.commit()

    login = client.post(
        "/login",
        json={"email": "john@example.com", "password": "123456"},
    )
    token = login.json()["token"]

    category = client.post(
        "/categories",
        json={"name": "Electronics"},
        headers={"Authorization": f"Bearer {token}"},
    ).json()

    product = client.post(
        "/products",
        json={
            "name": "Laptop",
            "price": 1000,
            "stock": 10,
            "category_id": category["id"],
        },
        headers={"Authorization": f"Bearer {token}"},
    ).json()

    client.post(
        "/cart",
        headers={"Authorization": f"Bearer {token}"},
    ).json()

    response = client.post(
        "/cart/items",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "product_id": product["id"],
            "quantity": 2,
            "unit_price": product["price"],
        },
    )

    assert response.status_code == 204

    response = client.get(
        "/cart/items",
        headers={"Authorization": f"Bearer {token}"},
    ).json()

    assert response["items"][0]["product_id"] == product["id"]
