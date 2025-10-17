import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)

def send_purchase_email(to_email, order):
    subject = "Confirmação do seu pedido"
    address = getattr(order, "address", None)
    payment = getattr(order, "payment_method", "Não informado")
    body = f"""
    Olá, seu pedido foi realizado com sucesso!

    Número do pedido: {order.id}
    Data: {getattr(order, 'order_date', getattr(order, 'created_at', ''))}
    Valor total: R$ {order.total_amount}

    Endereço de entrega:
    {address.street if address else ''}, {address.number if address else ''}
    {address.bairro if address else ''}  
    {address.city if address else ''} - {address.state if address else ''}
    CEP: {address.zip if address else ''}

    Forma de pagamento: {payment}

    Itens do pedido:
    """
    # Adapte para o modelo dos itens do pedido
    for item in getattr(order, "order_items", []):
        product_name = getattr(item, "product", None)
        if product_name:
            product_name = getattr(product_name, "name", "")
        else:
            product_name = getattr(item, "product_name", "")
        body += f"- {product_name} (Qtd: {item.quantity}) - R$ {item.unit_price}\n"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_FROM
    msg['To'] = to_email

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
        print(f"E-mail de pedido enviado para {to_email}")
    except Exception as e:
        print(f"Erro ao enviar e-mail de pedido: {e}")
