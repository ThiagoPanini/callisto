from dataclasses import dataclass

from app.src.features.get_tables_metadata.domain.entities.credentials import AccountCredentials
from app.src.features.get_tables_metadata.domain.entities.table_reference import TableReference


@dataclass
class InputDto:
    """
    Class representing the input data transfer object (DTO) for the use case.
    """
    tables_list: list[TableReference]
    credentials: AccountCredentials
