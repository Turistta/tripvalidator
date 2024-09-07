from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    latitude: Annotated[float, Field(ge=-90, le=90)]
    longitude: Annotated[float, Field(ge=-180, le=180)]


class Location(BaseModel):
    address: Annotated[str, Field()]
    plus_code: Annotated[Optional[str], Field(default=None)]
    coordinates: Annotated[Coordinates, Field()]


class Currency(BaseModel):
    code: Annotated[str, Field(min_length=3, max_length=3)]
    symbol: Annotated[str, Field()]
    name: Annotated[str, Field()]


class TransportationMethod(str, Enum):
    CAR = "CAR"
    PUBLIC_TRANSPORT = "PUBLIC_TRANSPORT"
    WALKING = "WALKING"
    BICYCLE = "BICYCLE"
