import json
from src.models.validator_models import TripValidatorOutput


class ValidatorParser:
    @staticmethod
    def parse_trip_validator_output(output_data: dict[str, any]) -> TripValidatorOutput:
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


