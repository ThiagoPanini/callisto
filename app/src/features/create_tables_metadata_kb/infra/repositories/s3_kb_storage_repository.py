import os
import json
import boto3

from app.src.features.create_tables_metadata_kb.domain.entities.kb_request import (
    TableMetadataKBRequest
)
from app.src.features.create_tables_metadata_kb.domain.entities.kb_output_content import (
    TableMetadataKBOutputContent
)
from app.src.features.create_tables_metadata_kb.domain.interfaces.kb_storage_repository_interface import (
    ITableMedatadaKBStorageRepository
)


class S3KBStorageRepository(ITableMedatadaKBStorageRepository):
    """
    Implementation of the metadata storage repository using S3.
    """

    def __init__(self):
        self.__client = boto3.client("s3")

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

        # Convert the list of TableMetadataKBOutputContent objects to a JSON string
        kb_content_json = [kb_content.to_dict() for kb_content in kb_output_content]

        # Store the metadata in S3
        self.__client.put_object(
            Bucket=os.getenv("KB_STORAGE_S3_BUCKET_NAME"),
            Key=f"knowledge_base/{kb_request.kb_id}.json",
            Body=json.dumps(kb_content_json, indent=4, ensure_ascii=False).encode("utf-8")
        )
