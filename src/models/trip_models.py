from datetime import datetime
from typing import Annotated, List

from pydantic import BaseModel, Field

from models.base_models import TransportationMethod
from models.cost_models import CostEstimate
from models.place_models import PlaceDetails


class TripSegment(BaseModel):
    start_point: Annotated[PlaceDetails, Field(description="Details of the starting point of the trip segment")]
    end_point: Annotated[PlaceDetails, Field(description="Details of the ending point of the trip segment")]
    departure_time: Annotated[
        datetime, Field(description="Departure time for the segment", examples=["2024-09-07T12:15:32.370Z"])
    ]
    arrival_time: Annotated[
        datetime, Field(description="Arrival time for the segment", examples=["2024-09-07T13:00:00.000Z"])
    ]
    cost_estimate: Annotated[CostEstimate, Field(description="Cost estimation for the segment")]
    transportation_method: Annotated[
        TransportationMethod, Field(description="Method of transportation for the segment", examples=["CAR"])
    ]


class Itinerary(BaseModel):
    segments: Annotated[List[TripSegment], Field(description="List of trip segments making up the full itinerary")]
    total_cost: Annotated[CostEstimate, Field(description="Total cost estimation for the full itinerary")]
    total_duration: Annotated[float, Field(ge=0, description="Total duration of the trip in hours", examples=[2.5])]


class UserPreference(BaseModel):
    category: Annotated[str, Field(description="Category of interest for the user", examples=["museum"])]
    weight: Annotated[float, Field(ge=0, le=1, description="Preference weight assigned by the user", examples=[0.8])]
