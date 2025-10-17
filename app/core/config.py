import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações de segurança
SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret")  # Chave secreta padrão
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")  # Algoritmo padrão para JWT
CRYPT_ALGORITHM = os.getenv("CRYPT_ALGORITHM", "HS256")  # Algoritmo para criptografia
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))  # Expiração do token de acesso
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))  # Expiração do refresh token
