from typing import Annotated

from fastapi import Body, FastAPI

from models.validator_models import TripValidatorRequest, TripValidatorResponse

app = FastAPI(title="TripValidator")


@app.post("/route")
def create_itinerary(request: Annotated[TripValidatorRequest, Body()]) -> TripValidatorResponse:
    pass
