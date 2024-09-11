from typing import Annotated, List

from pydantic import BaseModel, Field, HttpUrl

from models.base_models import Currency


class CostDetails(BaseModel):
    base_cost: Annotated[float, Field(ge=0, description="Base cost of the trip", examples=[10.0])]
    time_cost: Annotated[
        float, Field(ge=0, description="Cost associated with time spent during the trip", examples=[2.0])
    ]
    traffic_adjustment: Annotated[float, Field(ge=0, description="Adjustment factor based on traffic", examples=[1.2])]
    fuel_price: Annotated[float, Field(ge=0, description="Price of fuel per unit", examples=[4.5])]
    fuel_consumption: Annotated[
        float, Field(ge=0, description="Estimated fuel consumption for the trip", examples=[0.5])
    ]


class CostEstimate(BaseModel):
    source_urls: Annotated[
        List[HttpUrl],
        Field(description="Source URLs for cost estimation data", examples=[["https://example.com/fuel-prices"]]),
    ]
    source_description: Annotated[
        str, Field(description="Description of the source for cost data", examples=["Official Petrobrás website."])
    ]
    estimated_cost: Annotated[float, Field(ge=0, description="Estimated cost of the trip", examples=[12.5])]
    currency: Annotated[Currency, Field(description="Currency details for the cost estimate")]
    cost_details: Annotated[CostDetails, Field(description="Detailed breakdown of the cost estimate")]
