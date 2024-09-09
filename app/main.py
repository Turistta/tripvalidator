from fastapi import FastAPI
from dotenv import load_dotenv
import os


load_dotenv()
print(f"Chave OPEN AI carregada: {os.getenv('OPENAI_API_KEY')}")

from app.api.routes import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "API para validação de itinerários turísticos"}