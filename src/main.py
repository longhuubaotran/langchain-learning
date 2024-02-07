from fastapi import FastAPI
from routers import answer


app = FastAPI()

app.include_router(answer.router)
