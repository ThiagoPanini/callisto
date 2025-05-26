from abc import ABC, abstractmethod

from app.src.features.create_tables_metadata_kb.domain.entities.kb_request import (
    TableMetadataKBRequest
)
from app.src.features.create_tables_metadata_kb.domain.entities.kb_output_content import (
    TableMetadataKBOutputContent
)


class ITableMedatadaKBStorageRepository(ABC):
    """
    Interface for metadata storage repository.
    """

    @abstractmethod
    def store_knowledge_base(
        self,
        kb_request: TableMetadataKBRequest,
        kb_output_content: list[TableMetadataKBOutputContent]
    ) -> None:
        """
        Store knowledge base in the repository.

        :param kb_request: TableMetadataKBRequest object to be stored.
        :param kb_output_content: List of TableMetadataKBOutputContent objects to be stored.
        """
