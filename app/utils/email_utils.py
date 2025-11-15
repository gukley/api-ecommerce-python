import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)

def send_purchase_email(to_email, order):
    loja_nome = "GGTECH - Computadores e Periféricos"
    loja_email = SMTP_FROM
    loja_site = "https://ggtech.com.br"  # ou o domínio que planeja usar

    subject = f"🛒 {loja_nome} | Confirmação do Pedido #{order.id}"

    # Dados principais do pedido
    order_date = getattr(order, "order_date", getattr(order, "created_at", None))
    if isinstance(order_date, datetime):
        order_date = order_date.strftime("%d/%m/%Y %H:%M")

    address = getattr(order, "address", None)
    payment = getattr(order, "payment_method", "Não informado")

    # Cria corpo HTML do e-mail
    body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f6f6f6;
                color: #333;
                margin: 0;
                padding: 0;
            }}
            .container {{
                background-color: #fff;
                border-radius: 10px;
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .header {{
                background-color: #0d6efd;
                color: #fff;
                padding: 15px;
                border-radius: 10px 10px 0 0;
                text-align: center;
            }}
            .items {{
                margin-top: 15px;
                border-collapse: collapse;
                width: 100%;
            }}
            .items th, .items td {{
                border-bottom: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 13px;
                color: #666;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>{loja_nome}</h2>
                <p>Confirmação do seu pedido</p>
            </div>

            <p>Olá, seu pedido foi realizado com sucesso! 🎉</p>

            <p><strong>Número do pedido:</strong> {order.id}<br>
               <strong>Data:</strong> {order_date or '---'}<br>
               <strong>Valor total:</strong> R$ {order.total_amount:.2f}<br>
               <strong>Forma de pagamento: Cartão de Crédito</strong>
            </p>

            <h4>📦 Itens do Pedido:</h4>
            <table class="items">
                <tr>
                    <th>Produto</th>
                    <th>Qtd</th>
                    <th>Preço Unitário</th>
                </tr>
    """

    # Adiciona os itens do pedido dinamicamente
    for item in getattr(order, "order_items", []):
        product = getattr(item, "product", None)
        product_name = getattr(product, "name", getattr(item, "product_name", ""))
        body += f"""
            <tr>
                <td>{product_name}</td>
                <td>{item.quantity}</td>
                <td>R$ {item.unit_price:.2f}</td>
            </tr>
        """

    body += f"""
            </table>

            <h4>🏠 Endereço de Entrega:</h4>
            <p>
                {address.street if address else ''}, {address.number if address else ''}<br>
                {address.bairro if address else ''}<br>
                {address.city if address else ''} - {address.state if address else ''}<br>
                CEP: {address.zip if address else ''}
            </p>

            <div class="footer">
                <p>Obrigado por comprar na <strong>{loja_nome}</strong> 💙</p>
                <p>Em breve você receberá novas atualizações sobre o status do seu pedido.</p>
                <p><a href="{loja_site}">{loja_site}</a> | {loja_email}</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Monta e envia o e-mail
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = loja_email
    msg["To"] = to_email

    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(msg["From"], [msg["To"]], msg.as_string())
        print(f"[GGTECH] E-mail de confirmação enviado para {to_email}")
    except Exception as e:
        print(f"[GGTECH] Erro ao enviar e-mail: {e}")
