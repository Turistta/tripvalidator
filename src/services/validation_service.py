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
    TripSegment
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
        # Chaves adicionadas pra deixar no formato JSON
        headers = {"Authorization": f"Bearer {self.openai_api_key}", "Content-Type": "application/json"}
        prompt = f"""
        Validate the following travel itinerary and provide suggestions: {parsed_input.model_dump()}
        Return the response in the following JSON format:
        
        {{
            "header": {{
                "X-Processing-Time": float
            }},
            "payload": {{
                "output_data": {{
                    "is_valid": bool,
                    "validation_score": float,
                    "feedback": str,
                    "optimization_suggestions": [
                        {{
                            "original_segment": {{
                                "location": "Point A to Point B",
                                "distance": 120.5
                            }},
                            "suggested_segment": {{
                                "location": "Point A to Point C",
                                "distance": 100.0
                            }},
                            "reason": str,
                            "estimated_improvement": float
                        }}
                    ]
                }},
                "version": str
            }}
        }}
        """
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
                return result["payload"]["output_data"]

    def _map_segment(self, segment_data: dict) -> TripSegment:
        
        # Mapeia de JSON para objeto TripSegment
        # Campo distance adicionado no TripSegment
        location = segment_data.get("location", "")
        start_point, end_point = location.split(" to ")

        return TripSegment(
            start_point=PlaceDetails(name=start_point),
            end_point=PlaceDetails(name=end_point),
            distance=segment_data.get("distance", 0.0)
        )

    def _calculate_estimated_improvement(self, original_segment: TripSegment, suggested_segment: TripSegment) -> float:
        
        # Se houver melhoria na distancia percorrido entre os itinerarios
        # Calcula e retorna o percentual de melhoria
        original_distance = original_segment.distance
        suggested_distance = suggested_segment.distance

        if original_distance == 0:
            return 0.0

        improvement = ((original_distance - suggested_distance) / original_distance) * 100
        return max(improvement, 0.0)  # Retorna 0 se não houver melhoria

    def _process_ai_results(self, ai_results: dict) -> TripValidatorResponse:
        suggestions = ai_results.get("optimization_suggestions", [])
        is_valid = ai_results.get("is_valid", False)
        validation_score = ai_results.get("validation_score", 0.0)
        feedback = ai_results.get("feedback", "")

        optimization_suggestions = []
        for suggestion in suggestions:
            original_segment_data = suggestion.get("original_segment", {})
            suggested_segment_data = suggestion.get("suggested_segment", {})

            # Mapeando os segmentos dos itinerarios original e sugerido
            original_segment = self._map_segment(original_segment_data)
            suggested_segment = self._map_segment(suggested_segment_data)

            # Calculando a melhoria estimada atribuido em estimated_improvement
            estimated_improvement = self._calculate_estimated_improvement(original_segment, suggested_segment)

            optimization_suggestions.append(
                OptimizationSuggestion(
                    original_segment=original_segment,
                    suggested_segment=suggested_segment,
                    reason=suggestion.get("reason", ""),
                    estimated_improvement=estimated_improvement,
                )
            )

        output_data = TripValidatorOutput(
            is_valid=is_valid,
            validation_score=validation_score,
            feedback=feedback,
            optimization_suggestions=optimization_suggestions,
        )

        return TripValidatorResponse(output_data=output_data, processing_time=0.0, version="1.0.0")