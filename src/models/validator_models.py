from typing import Annotated, List, Optional

from pydantic import BaseModel, Field

from models.trip_models import Itinerary, TripSegment, UserPreference


class TripValidatorInput(BaseModel):
    itinerary: Annotated[Itinerary, Field(description="Proposed trip itinerary for validation")]
    user_preferences: Annotated[List[UserPreference], Field(description="List of user preferences for the itinerary")]


class OptimizationSuggestion(BaseModel):
    original_segment: Annotated[TripSegment, Field(description="Original trip segment before optimization")]
    suggested_segment: Annotated[TripSegment, Field(description="Suggested optimized trip segment")]
    reason: Annotated[str, Field(description="Reason for the suggested optimization", examples=["Reduced travel time"])]
    estimated_improvement: Annotated[
        float, Field(ge=0, description="Estimated improvement in percentage", examples=[15.0])
    ]


class TripValidatorOutput(BaseModel):
    is_valid: Annotated[bool, Field(description="Indicates whether the proposed itinerary is valid")]
    validation_score: Annotated[
        float, Field(ge=0, le=1, description="Score indicating the confidence level of validation", examples=[0.95])
    ]
    feedback: Annotated[
        str,
        Field(
            description="Feedback from the validator regarding the proposed itinerary",
            examples=["The itinerary is feasible but can be optimized for time."],
        ),
    ]
    optimization_suggestions: Annotated[
        Optional[List[OptimizationSuggestion]],
        Field(default=None, description="List of suggestions for optimizing the itinerary"),
    ]


class TripValidatorRequest(BaseModel):
    input_data: Annotated[TripValidatorInput, Field(description="Input data for the trip validation request")]


class TripValidatorResponse(BaseModel):
    output_data: Annotated[TripValidatorOutput, Field(description="Output data for the trip validation response")]
    processing_time: Annotated[
        float, Field(ge=0, description="Time taken to process the validation in seconds", examples=[1.25])
    ]
    version: Annotated[
        str, Field(pattern=r"^\d+\.\d+\.\d+$", description="Version of the TripValidator service", examples=["1.0.0"])
    ]
