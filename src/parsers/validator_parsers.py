import json
import requests

from src.models.validator_models import TripValidatorResponse
from src.models.validator_models import TripValidatorOutput

#TODO: Modificar o input esperado pela NLP e configurar o output para o formato esperado 
"""
Formato esperado:
HEADER
X-Processing-Time: float
---------------
PAYLOAD
{
output_data: {
    is_valid: bool,
    validation_score: float,
    feedback: str,
    optimization_suggestions: List[OptimizationSuggestion],
    },

version: str,
}

"""

class ValidatorParser:
    @staticmethod
    def parse(response: requests.Response) -> TripValidatorResponse:
        payload = response.json()
        headers = response.headers

        return TripValidatorResponse(
            output_data=ValidatorParser._parse_trip_validator_output(payload["output_data"]),
            processing_time=ValidatorParser._parse_processing_time_tripvalidator(headers),
            version=ValidatorParser._parse_version_tripvalidator(payload),
        )

    @staticmethod
    def _parse_trip_validator_output(output_data: dict[str, any]) -> TripValidatorOutput:
        try:
            json_output = json.loads(output_data)
            if "is_valid" not in json_output:
                raise ValueError("The validator output data must contain the 'is_valid' field.")
            if "validation_score" not in json_output:
                raise ValueError("The validator output data must contain the 'validation_score' field.")
            if "feedback" not in json_output:
                raise ValueError("The validator output data must contain the 'feedback' field.")
            if "optimization_suggestions" not in json_output:
                raise ValueError("The validator output data must contain the 'optimization_suggestions' field.")
            
            return TripValidatorOutput(
                is_valid=output_data["is_valid"],
                validation_score=output_data["validation_score"],
                feedback=output_data["feedback"],
                optimization_suggestions=output_data["optimization_suggestions"],
            )

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse the validator output data: {e}")


    @staticmethod
    def _parse_version_tripvalidator(output_data: str) -> str:
        try:
            json_output = json.loads(output_data)
            if "version" not in json_output:
                raise ValueError("The validator output data must contain the 'version' field.")
            
            return output_data["version"]

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse the validator output data: {e}")


    @staticmethod
    def _parse_processing_time_tripvalidator(headers: dict[str, str]) -> float:
        # Verifica se o cabeçalho "X-Processing-Time" está presente na resposta
        processing_time = headers.get('X-Processing-Time')
        if processing_time:
            return float(processing_time) 
        else:
            raise ValueError("The response does not contain the 'X-Processing-Time' header.")
