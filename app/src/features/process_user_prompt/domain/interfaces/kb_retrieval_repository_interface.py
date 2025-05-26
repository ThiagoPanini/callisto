from abc import ABC, abstractmethod
from typing import Any


class IKBRetrievalRepository(ABC):
    """
    Interface for Knowledge Base Retrieval Repository.
    """

    @abstractmethod
    def retrieve_knowledge_base(self, kb_id: str) -> list[dict[str, Any]]:
        """
        Retrieve relevant documents from the knowledge base based on the query.

        :param kb_id: The ID of the knowledge base to retrieve.
        :return: A list of table metadata information.
        """
