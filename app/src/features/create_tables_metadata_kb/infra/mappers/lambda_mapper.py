import json
from typing import Any

from app.src.features.create_tables_metadata_kb.domain.entities.kb_input_reference import (
    TableMetadataKBInputReference
)
from app.src.features.create_tables_metadata_kb.domain.dtos.input_dto import (
    CreateTablesMetadataKBInputDTO
)
from app.src.features.cross.domain.entities.credentials import AccountCredentials


class LambdaMapper:
    """
    Mapper class to convert between Lambda event data and the input DTO for the use case.
    """

    def get_input_dto_from_lambda_event(self, event: dict[str, Any]) -> CreateTablesMetadataKBInputDTO:
        """
        Convert a Lambda event to a CreateTablesMetadataKBInputDTO.

        :param event: The Lambda event data.
        :return: An instance of CreateTablesMetadataKBInputDTO.
        """

        # Extracting the body from the event
        body = json.loads(event["body"])

        # Building entities for input dto
        kb_input_refence = [
            TableMetadataKBInputReference(**table) for table in body["kb_input_refence"]
        ]
        account_credentials = AccountCredentials(**body["account_credentials"])

        return CreateTablesMetadataKBInputDTO(
            tables_list=kb_input_refence,
            account_credentials=account_credentials
        )
