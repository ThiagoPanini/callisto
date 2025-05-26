import os
import json
from typing import Any

import boto3

from app.src.features.process_user_prompt.domain.interfaces.kb_retrieval_repository_interface import (
    IKBRetrievalRepository
)
from app.src.features.create_tables_metadata_kb.domain.entities.kb_output_content import TableMetadataKBOutputContent


class S3KBRetrievalRepository(IKBRetrievalRepository):
    """
    Implementation of the knowledge base retrieval repository using S3.
    """

    def __init__(self):
        self.__client = boto3.client("s3")

    def retrieve_knowledge_base(self, kb_id: str) -> list[dict[str, Any]]:
        """
        Retrieve knowledge base from the repository.

        :param kb_id: Unique identifier for the knowledge base.
        :return: Knowledge base content as a dictionary.
        """

        response = self.__client.get_object(
            Bucket=os.getenv("KB_STORAGE_S3_BUCKET_NAME"),
            Key=f"knowledge_base/{kb_id}.json"
        )

        return json.loads(response["Body"].read())
