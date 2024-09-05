from fastapi import FastAPI
from dotenv import load_dotenv
import os
from app.api.routes import router

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
print(os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Incluir as rotas da aplicação
app.include_router(router)

# Adicionar root route opcionalmente
@app.get("/")
def read_root():
    return {"message": "API para validação de itinerários turísticos"}