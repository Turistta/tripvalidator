import logging
import time
from ast import parse
from datetime import datetime
from typing import Annotated, Any, List

import aiohttp
from aiohttp import ClientConnectionError
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
from parsers.validator_parsers import ValidatorParser

logger = logging.getLogger(__name__)


class ValidationService:
    def __init__(self):
        self.openai_api_key = settings.openai_api_key  # type: ignore
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not configured correctly.")
        self.openai_api_url = "https://api.openai.com/v1/chat/completions"
        self.ai_results_parser = ValidatorParser()

    async def validate_itinerary(self, client_data: TripValidatorInput) -> TripValidatorResponse:
        try:
            ai_prompt_data_request = self._build_ai_request(client_data)
            ai_validation_results = await self._ai_request_validation(ai_prompt_data_request)
            processed_results = self._process_ai_results(validation_results=ai_validation_results)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=f"Invalid input data: {str(e)}")
        except Exception as e:
            raise e

        return processed_results

    def _build_ai_request(self, input_data: TripValidatorInput) -> dict[str, Any]:
        """Builds input data and prompt for requesting to the AI model."""

        prompt = f"""
        Validate the following travel itinerary and provide suggestions: {input_data.model_dump()}
        Return the response in the following format:
        
        HEADER
        X-Processing-Time: float
        ---------------
        PAYLOAD
        
            "output_data":
                "is_valid": bool,
                "validation_score": float,
                "feedback": str,
                "optimization_suggestions": [
                    
                    "original_segment":
                    "suggested_segment":
                    "reason":
                    "estimated_improvement":
                
                ],

                In original_segment, put the original itinerary, in suggested_segment, put the suggestions
            ,
            "version": str
        
        """
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a travel assistant specialized in validating itineraries."},
                {"role": "user", "content": prompt},
            ],
        }

        return data

    async def _ai_request_validation(self, data: dict[str, Any]) -> dict:
        headers = {"Authorization": f"Bearer {self.openai_api_key}", "Content-Type": "application/json"}
        async with aiohttp.ClientSession() as session:
            endpoint = self.openai_api_url
            try:
                async with session.post(self.openai_api_url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(result)
                        return {"suggestions": result["choices"][0]["message"]["content"]}
                    logger.error(msg := f"{__name__} raised for status: {response.status}")
                    raise HTTPException(status_code=response.status, detail=msg)
            except (ClientConnectionError, HTTPException) as e:
                logger.error(f"Request error for URL {endpoint}: {e}")
                raise e

    def _process_ai_results(self, validation_results: dict[str, Any]) -> TripValidatorResponse:
        # TODO: Use the ai_validation_parser here and implement processing.

        try:
            parsed_results = self.ai_results_parser.parse(validation_results)
            print(parsed_results)
        except:
            pass

        suggestions = validation_results.get("suggestions", "")
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
