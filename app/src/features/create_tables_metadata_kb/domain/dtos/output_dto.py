from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class CreateTablesMetadataKBOutputDTO:
    """
    Class representing the output data transfer object (DTO) for the use case.
    """
    status_code: str
    headers: Optional[dict[str, Any]] = None
    body: Optional[dict[str, Any]] = None
