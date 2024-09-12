import json
import logging
from datetime import datetime
from json import JSONDecodeError
from typing import Any, Dict, List
from xml.etree.ElementTree import parse

from pydantic import BaseModel, EmailStr, HttpUrl
from typing_extensions import Annotated, Optional

from models.base_models import Currency, Location, TransportationMethod
from models.cost_models import CostDetails, CostEstimate
from models.place_models import Picture, PlaceDetails, Review, ReviewAuthor
from models.trip_models import TripSegment
from models.validator_models import (
    OptimizationSuggestion,
    TripValidatorOutput,
    TripValidatorResponse,
)

logger = logging.getLogger(__name__)


class ValidationParser:
    @staticmethod
    def parse(response: str) -> TripValidatorOutput:
        try:
            json_response = json.loads(response)
            response_str = json_response["choices"][0]["message"]["content"]
            formatted_str = "\n".join(response_str.split("\n")[1:-1])
            parsed_response = json.loads(formatted_str)
            print(parsed_response)

            # TODO: Fix parsers at model level.

            # optimization_suggestions = [
            #     ValidationParser.parse_optimization_suggestion(suggestion)
            #     for suggestion in output_data.get("optimization_suggestions", [])
            # ]

            # return TripValidatorOutput(
            #     is_valid=output_data.get("is_valid", False),
            #     validation_score=output_data.get("validation_score", 0.0),
            #     feedback=output_data.get("feedback", ""),
            #     optimization_suggestions=optimization_suggestions,
            # )
        except (JSONDecodeError, KeyError) as e:
            logger.error(f"Error parsing API response: {e}")
            raise e

    # @staticmethod
    # def parse_optimization_suggestion(suggestion: Dict[str, Any]) -> OptimizationSuggestion:
    #     return OptimizationSuggestion(
    #         original_segment=ValidationParser.parse_trip_segment(suggestion.get("original_segment", {})),
    #         suggested_segment=ValidationParser.parse_trip_segment(suggestion.get("suggested_segment", {})),
    #         reason=suggestion.get("reason", ""),
    #         estimated_improvement=float(suggestion.get("estimated_improvement", 0)),
    #     )

    # @staticmethod
    # def parse_trip_segment(segment_data: Dict[str, Any]) -> TripSegment:
    #     return TripSegment(
    #         start_point=ValidationParser.parse_place_details(segment_data.get("start_point", {})),
    #         end_point=ValidationParser.parse_place_details(segment_data.get("end_point", {})),
    #         departure_time=datetime.fromisoformat(segment_data.get("departure_time", "")),
    #         arrival_time=datetime.fromisoformat(segment_data.get("arrival_time", "")),
    #         cost_estimate=ValidationParser.parse_cost_estimate(segment_data.get("cost_estimate", {})),
    #         transportation_method=segment_data.get("transportation_method", ""),
    #     )

    # @staticmethod
    # def parse_place_details(place_data: Dict[str, Any]) -> PlaceDetails:
    #     return PlaceDetails(
    #         place_id=place_data.get("place_id", ""),
    #         name=place_data.get("name", ""),
    #         location=Location(**place_data.get("location", {})),
    #         types=place_data.get("types", []),
    #         reviews=[ValidationParser.parse_review(review) for review in place_data.get("reviews", [])],
    #         pictures=[ValidationParser.parse_picture(picture) for picture in place_data.get("pictures", [])],
    #         ratings_total=place_data.get("ratings_total", 0),
    #     )

    # @staticmethod
    # def parse_review(review_data: Dict[str, Any]) -> Review:
    #     return Review(
    #         author=ReviewAuthor(**review_data.get("author", {})),
    #         rating=review_data.get("rating", 0.0),
    #         text=review_data.get("text", ""),
    #         language=review_data.get("language", ""),
    #         publication_time=datetime.fromisoformat(review_data.get("publication_time", "")),
    #     )

    # @staticmethod
    # def parse_picture(picture_data: Dict[str, Any]) -> Picture:
    #     return Picture(**picture_data)

    # @staticmethod
    # def parse_cost_estimate(cost_data: Dict[str, Any]) -> CostEstimate:
    #     return CostEstimate(
    #         source_urls=cost_data.get("source_urls", []),
    #         source_description=cost_data.get("source_description", ""),
    #         estimated_cost=cost_data.get("estimated_cost", 0.0),
    #         currency=Currency(**cost_data.get("currency", {})),
    #         cost_details=CostDetails(**cost_data.get("cost_details", {})),
    #     )
