import smtplib
from email.mime.text import MIMEText

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "gustavokley08@gmail.com"
SMTP_PASSWORD = "SUA_SENHA_DE_APP"  # Use senha de app se 2FA ativado

msg = MIMEText("Teste de envio de e-mail via Python")
msg['Subject'] = "Teste SMTP"
msg['From'] = SMTP_USER
msg['To'] = SMTP_USER

try:
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
    print("E-mail enviado com sucesso!")
except Exception as e:
    print(f"Erro ao enviar e-mail: {e}")
