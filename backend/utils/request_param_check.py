

import requests
from backend.utils.custom_exceptions import InvalidURLException


def check_url(pdf_path):
    try:
        if pdf_path.startswith("http//") or pdf_path.startswith("https://"):
            response = requests.get(pdf_path)
            if response.status_code!=200:
                return False
        return True
             
    except Exception as e:
        return False