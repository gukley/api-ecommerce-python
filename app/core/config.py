import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
CRYPT_ALGORITHM = os.getenv("CRYPT_ALGORITHM", "HS256")
