from abc import ABC, abstractmethod
from typing import Optional

from app.src.features.create_tables_metadata_kb.domain.entities.kb_request import (
    TableMetadataKBRequest
)
from app.src.features.create_tables_metadata_kb.domain.entities.kb_output_content import (
    TableMetadataKBOutputContent
)
from app.src.features.cross.domain.entities.credentials import AccountCredentials


class ITableMetadataKBRetrievalAdapter(ABC):

    @abstractmethod
    def get_knowledge_base(
        self,
        kb_request: TableMetadataKBRequest,
        account_credentials: AccountCredentials
    ) -> Optional[list[TableMetadataKBOutputContent]]:
        """
        Retrieve knowledge base from the repository.

        :param kb_request: TableMetadataKBRequest object to be retrieved.
        :param account_credentials: AccountCredentials object containing requester credentials.

        :return: List of TableMetadataKBOutputContent objects if found, None otherwise.
        """
