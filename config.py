from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
SENDER_TAX_ID = os.getenv("SENDER_TAX_ID")
SENDER_SYSTEM_ID = os.getenv("SENDER_SYSTEM_ID")
COUNTRY_CODE = os.getenv("COUNTRY_CODE")
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
RETRY_LIMIT = int(os.getenv('RETRY_LIMIT') or 3)
SAMPLE_DOCUMENT_ID = os.getenv('SAMPLE_DOCUMENT_ID')