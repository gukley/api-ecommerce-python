from app.utils.email_utils import send_purchase_email

class Item:
    def __init__(self, product_name, quantity, price):
        self.product_name = product_name
        self.quantity = quantity
        self.price = price

class Order:
    def __init__(self):
        self.id = 123
        self.created_at = "2024-06-01"
        self.total = 99.90
        self.items = [Item("Produto Teste", 2, 49.95)]

send_purchase_email("seuemail@dominio.com", Order())
