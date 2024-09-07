from typing import Annotated, List, Optional

from pydantic import BaseModel, Field

from models.trip_models import Itinerary, TripSegment, UserPreference


class TripValidatorInput(BaseModel):
    itinerary: Annotated[Itinerary, Field()]
    user_preferences: Annotated[List[UserPreference], Field()]


class OptimizationSuggestion(BaseModel):
    original_segment: Annotated[TripSegment, Field()]
    suggested_segment: Annotated[TripSegment, Field()]
    reason: Annotated[str, Field()]
    estimated_improvement: Annotated[float, Field(ge=0)]


class TripValidatorOutput(BaseModel):
    is_valid: Annotated[bool, Field()]
    validation_score: Annotated[float, Field(ge=0, le=1)]
    feedback: Annotated[str, Field()]
    optimization_suggestions: Annotated[Optional[List[OptimizationSuggestion]], Field(default=None)]


class TripValidatorRequest(BaseModel):
    input_data: Annotated[TripValidatorInput, Field()]


class TripValidatorResponse(BaseModel):
    output_data: Annotated[TripValidatorOutput, Field()]
    processing_time: Annotated[float, Field(ge=0)]
    version: Annotated[str, Field(pattern=r"^\d+\.\d+\.\d+$")]
