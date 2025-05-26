from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.src.features.create_tables_metadata_kb.domain.entities.kb_input_reference import (
    TableMetadataKBInputReference
)
from app.src.features.cross.domain.value_objects import (
    KBType,
    ProcessingStatus
)


@dataclass
class TableMetadataKBRequest:
    """
    Class representing a knowledge base.
    """
    kb_id: str
    kb_input_refence: list[TableMetadataKBInputReference]
    datetime_creation: datetime
    datetime_last_update: datetime = None
    kb_type: KBType = KBType.TABLE_METADATA
    status: ProcessingStatus = ProcessingStatus.PENDING
    kb_storage_uri: Optional[str] = None
