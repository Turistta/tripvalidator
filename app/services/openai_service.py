import httpx
import os
from fastapi import HTTPException

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise HTTPException(status_code=500, detail="Chave de API da OpenAI não configurada corretamente.")

async def validate_itinerary(itinerary: dict) -> dict:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"Valide o seguinte itinerário turístico e faça sugestões: {itinerary}"

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Você é um assistente de viagem."},
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions", 
            headers=headers, 
            json=data
        )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Erro ao validar o itinerário: {response.text}")

    
        result = response.json()
        suggestions = result['choices'][0]['message']['content']

        return {"itinerary": itinerary, "suggestions": suggestions}