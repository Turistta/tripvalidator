from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
print(os.getenv("OPENAI_API_KEY"))

from app.api.routes import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "API para validação de itinerários turísticos"}