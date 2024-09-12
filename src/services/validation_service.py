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
from parsers.validator_parsers import ValidationParser

logger = logging.getLogger(__name__)


class ValidationService:
    def __init__(self):
        self.openai_api_key = settings.openai_api_key  # type: ignore
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not configured correctly.")
        self.openai_api_url = "https://api.openai.com/v1/chat/completions"
        self.ai_results_parser = ValidationParser()

    async def validate_itinerary(self, client_data: TripValidatorInput) -> TripValidatorResponse:
        try:
            ai_prompt_data_request = self._build_ai_request(client_data)
            ai_validation_results = await self._ai_request_validation(ai_prompt_data_request)
            parsed_results = self.ai_results_parser.parse(ai_validation_results)
            processed_results = self._process_ai_results(parsed_results=parsed_results)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=f"Invalid input data: {str(e)}")
        except Exception as e:
            raise e

        return processed_results

    def _build_ai_request(self, input_data: TripValidatorInput) -> dict[str, Any]:
        """Builds input data and prompt for requesting to the AI model."""

        prompt = f"""
        Validate the following travel itinerary and provide suggestions: {input_data.model_dump()}
        Give the response in the following json format:
        
        "output_data":
            "feedback": str,
            "optimization_suggestions": [
                "original_segment":
                "suggested_segment":
                "reason":
                "estimated_improvement":
            ],

        In original_segment, put the original itinerary, in suggested_segment, put the suggestions.       
        """
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a travel assistant specialized in validating itineraries."},
                {"role": "user", "content": prompt},
            ],
        }

        return data

    async def _ai_request_validation(self, data: dict[str, Any]) -> str:
        headers = {"Authorization": f"Bearer {self.openai_api_key}", "Content-Type": "application/json"}
        async with aiohttp.ClientSession() as session:
            endpoint = self.openai_api_url
            try:
                async with session.post(self.openai_api_url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.text()
                        return result
                    logger.error(msg := f"{__name__} raised for status: {response.status}")
                    raise HTTPException(status_code=response.status, detail=msg)
            except (ClientConnectionError, HTTPException) as e:
                logger.error(f"Request error for URL {endpoint}: {e}")
                raise e

    def _process_ai_results(self, parsed_results: TripValidatorOutput) -> TripValidatorResponse:
        processed_results = TripValidatorResponse(
            output_data=parsed_results,
            processing_time=0,  # TODO: Calculate total processing time
            version="1.0.0",  # TODO: Give a version to this revision based on id (future implementation)
        )

        return processed_results
