import time
from typing import Annotated

from fastapi import Body, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from models.validator_models import TripValidatorRequest, TripValidatorResponse
from services.validation_service import ValidationService

app = FastAPI(title="TripValidator")


@app.post("/route")
async def create_itinerary(request: Annotated[TripValidatorRequest, Body()]) -> TripValidatorResponse:
    start_time = time.time()
    validation_service = ValidationService()
    try:
        response = await validation_service.validate_itinerary(request.input_data)
        processing_time = time.time() - start_time
        response.processing_time = processing_time
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=422, content={"detail": str(exc)})
