import os
from dotenv import load_dotenv

load_dotenv()

BASE_API_URL = os.getenv('BASE_API_URL')

DEFAULT_JSON_HEADERS = {'Content-Type': 'application/json',
                        "Accept": "application/json"}
