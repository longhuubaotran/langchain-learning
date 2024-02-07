import requests
from fastapi import APIRouter
from configs import get_session_with_headers
router = APIRouter()


@router.post("/answer")
async def get_answer(prompt: str):
    session = get_session_with_headers()
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"{prompt}"}],
        "temperature": 0.7
    }
    response = session.post(
        "https://api.openai.com/v1/chat/completions", json=payload)
    return response.json()
