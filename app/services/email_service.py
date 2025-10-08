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

def send_reset_email(to_email: str, token: str):
    subject = "Recuperação de senha"
    reset_link = f"http://localhost:8001/reset-password?token={token}"
    body = f"""
    Olá,
    
    Você solicitou a recuperação de senha. Clique no link abaixo para redefinir sua senha:
    {reset_link}
    
    Se você não solicitou, ignore este e-mail.
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_FROM
    msg['To'] = to_email

    print(f"[DEBUG] Chamando envio de e-mail para {to_email}")
    print(f"[DEBUG] SMTP config: host={SMTP_HOST}, port={SMTP_PORT}, user={SMTP_USER}")
    print(f"[DEBUG] Conteúdo do e-mail: {body}")

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
        print(f"E-mail de recuperação enviado para {to_email}")
    except Exception as e:
        print(f"Erro ao enviar e-mail de recuperação: {e}")
