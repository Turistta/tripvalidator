from datetime import datetime, time
from enum import Enum
from typing import Annotated, Dict, List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl


# Enum for transportation methods
class TransportationMethod(str, Enum):
    CAR = "CAR"
    PUBLIC_TRANSPORT = "PUBLIC_TRANSPORT"
    WALKING = "WALKING"
    BICYCLE = "BICYCLE"


class Coordinates(BaseModel):
    latitude: Annotated[float, Field(ge=-90, le=90, description="Latitude of the location", examples=[40.7128])]
    longitude: Annotated[float, Field(ge=-180, le=180, description="Longitude of the location", examples=[-74.0060])]


class Location(BaseModel):
    address: Annotated[
        str,
        Field(
            description="Full address of the location", examples=["Av. Deputado Jamel Cecílio, Goiânia - GO, Brasil"]
        ),
    ]
    plus_code: Annotated[
        Optional[str],
        Field(default=None, description="Google Plus Code for the location", examples=["34MP+FJ Goiânia, GO, Brasil"]),
    ]
    coordinates: Annotated[Coordinates, Field(description="Geographical coordinates of the location")]


class Currency(BaseModel):
    code: Annotated[
        str, Field(min_length=3, max_length=3, description="Currency code in ISO 4217 format", examples=["USD"])
    ]
    symbol: Annotated[str, Field(description="Symbol representing the currency", examples=["$"])]
    name: Annotated[str, Field(description="Full name of the currency", examples=["US Dollar"])]
