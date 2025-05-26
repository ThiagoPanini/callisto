import json
from typing import Any

from app.src.features.process_user_prompt.domain.dtos.input_dto import ProcessUserPromptInputDTO
from app.src.features.cross.domain.entities.credentials import AccountCredentials


class LambdaMapper:
    """
    Mapper class to convert between Lambda event data and the input DTO for the use case.
    """

    def get_input_dto_from_lambda_event(self, event: dict[str, Any]) -> ProcessUserPromptInputDTO:
        """
        Convert a Lambda event to a ProcessUserPromptInputDTO.

        :param event: The Lambda event data.
        :return: An instance of ProcessUserPromptInputDTO.
        """

        # Extracting the body from the event
        body = json.loads(event["body"])

        # Building entities for input dto
        user_prompt = body["user_prompt"]
        kb_id = body["kb_id"]
        account_credentials = AccountCredentials(**body["account_credentials"])

        return ProcessUserPromptInputDTO(
            user_prompt=user_prompt,
            kb_id=kb_id,
            account_credentials=account_credentials
        )
