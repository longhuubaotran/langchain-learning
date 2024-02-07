from dotenv import load_dotenv
import os
import requests


def get_session_with_headers():
    session = requests.Session()

    load_dotenv()
    headers = {'Content-Type': 'application/json',
               'Authorization': f"{os.getenv('BEARER_OPENAI_API_KEY')}"}
    session.headers.update(headers)
    return session
