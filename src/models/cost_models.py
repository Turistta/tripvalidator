from typing import Annotated, List

from pydantic import BaseModel, Field, HttpUrl

from models.base_models import Currency


class CostDetails(BaseModel):
    base_cost: Annotated[float, Field(ge=0)]
    time_cost: Annotated[float, Field(ge=0)]
    traffic_adjustment: Annotated[float, Field(ge=0)]
    fuel_price: Annotated[float, Field(ge=0)]
    fuel_consumption: Annotated[float, Field(ge=0)]


class CostEstimate(BaseModel):
    source_urls: Annotated[List[HttpUrl], Field()]
    source_description: Annotated[str, Field()]
    estimated_cost: Annotated[float, Field(ge=0)]
    currency: Annotated[Currency, Field()]
    cost_details: Annotated[CostDetails, Field()]
