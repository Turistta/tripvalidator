from datetime import datetime
from typing import Annotated, List

from pydantic import BaseModel, Field

from models.base_models import TransportationMethod
from models.cost_models import CostEstimate
from models.place_models import PlaceDetails


class TripSegment(BaseModel):
    start_point: Annotated[PlaceDetails, Field()]
    end_point: Annotated[PlaceDetails, Field()]
    departure_time: Annotated[datetime, Field()]
    arrival_time: Annotated[datetime, Field()]
    cost_estimate: Annotated[CostEstimate, Field()]
    transportation_method: Annotated[TransportationMethod, Field()]


class Itinerary(BaseModel):
    segments: Annotated[List[TripSegment], Field()]
    total_cost: Annotated[CostEstimate, Field()]
    total_duration: Annotated[float, Field(ge=0)]


class UserPreference(BaseModel):
    category: Annotated[str, Field()]
    weight: Annotated[float, Field(ge=0, le=1)]
