from dataclasses import dataclass

from app.src.features.create_tables_metadata_kb.domain.entities.kb_input_reference import TableMetadataKBInputReference
from app.src.features.cross.domain.entities.credentials import AccountCredentials


@dataclass
class CreateTablesMetadataKBInputDTO:
    """
    Class representing the input data transfer object (DTO) for the use case.
    """
    tables_list: list[TableMetadataKBInputReference]
    account_credentials: AccountCredentials
