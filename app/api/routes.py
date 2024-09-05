from fastapi import APIRouter, HTTPException
from app.services.openai_service import validate_itinerary

router = APIRouter()

@router.get("/validar/")
async def get_validated_itinerary(itinerary: dict):
    try:
        validated_itinerary = await validate_itinerary(itinerary)
        return validated_itinerary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))