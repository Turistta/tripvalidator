import time
from datetime import datetime
from typing import Annotated, List

import aiohttp
from fastapi import HTTPException
from pydantic import BaseModel, Field, ValidationError

from core.config import settings
from models.base_models import TransportationMethod
from models.cost_models import CostEstimate
from models.place_models import PlaceDetails
from models.validator_models import (
    OptimizationSuggestion,
    TripValidatorInput,
    TripValidatorOutput,
    TripValidatorRequest,
    TripValidatorResponse,
)


class ValidationService:
    def __init__(self):
        self.openai_api_key = settings.openai_api_key  # type: ignore
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not configured correctly.")
        self.openai_api_url = "https://api.openai.com/v1/chat/completions"

    async def validate_itinerary(self, input_data: TripValidatorInput) -> TripValidatorResponse:
        try:
            parsed_input = self._parse_input(input_data)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=f"Invalid input data: {str(e)}")
        ai_validation_result = await self._ai_validate(parsed_input)
        validation_output = self._process_ai_results(ai_validation_result)

        return validation_output

    def _parse_input(self, input_data: TripValidatorInput) -> TripValidatorInput:
        return input_data

    async def _ai_validate(self, parsed_input: TripValidatorInput) -> dict:
        headers = {"Authorization": f"Bearer {self.openai_api_key}", "Content-Type": "application/json"}
        prompt = f"Validate the following travel itinerary and provide suggestions: {parsed_input.model_dump()}"
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a travel assistant specialized in validating itineraries."},
                {"role": "user", "content": prompt},
            ],
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.openai_api_url, headers=headers, json=data) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status, detail=f"Error validating itinerary: {await response.text()}"
                    )

                result = await response.json()
                return {"suggestions": result["choices"][0]["message"]["content"]}

    def _process_ai_results(self, ai_results: dict) -> TripValidatorResponse:
        suggestions = ai_results.get("suggestions", "")
        is_valid = "valid" in suggestions.lower() and "invalid" not in suggestions.lower()
        validation_score = 0.9 if is_valid else 0.5

        optimization_suggestions = []
        if "suggestions:" in suggestions.lower():
            suggestion_text = suggestions.split("suggestions:")[1].strip()
            optimization_suggestions.append(
                OptimizationSuggestion(
                    original_segment=None,  # TODO: map suggestion to respective segment.  # type: ignore
                    suggested_segment=None,  # type: ignore
                    reason=suggestion_text,
                    estimated_improvement=10.0,  # TODO: Calculate actual value
                )
            )

        output_data = TripValidatorOutput(
            is_valid=is_valid,
            validation_score=validation_score,
            feedback=suggestions,
            optimization_suggestions=optimization_suggestions,
        )

        return TripValidatorResponse(output_data=output_data, processing_time=0.0, version="1.0.0")
