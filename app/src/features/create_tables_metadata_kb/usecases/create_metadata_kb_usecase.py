from uuid import uuid4
from datetime import datetime, timezone

from app.src.features.cross.utils.logger import setup_logger
from app.src.features.create_tables_metadata_kb.domain.dtos.input_dto import (
    CreateTablesMetadataKBInputDTO
)
from app.src.features.create_tables_metadata_kb.domain.dtos.output_dto import (
    CreateTablesMetadataKBOutputDTO
)
from app.src.features.create_tables_metadata_kb.domain.entities.kb_request import (
    TableMetadataKBRequest
)
from app.src.features.create_tables_metadata_kb.domain.interfaces.kb_retrieval_adapter_interface import (
    ITableMetadataKBRetrievalAdapter
)
from app.src.features.create_tables_metadata_kb.domain.interfaces.kb_storage_repository_interface import (
    ITableMedatadaKBStorageRepository
)


class CreateTablesMetadataKBUseCase:
    """
    Use case for creating metadata knowledge base.
    """

    def __init__(
        self,
        kb_retrieval_adapter: ITableMetadataKBRetrievalAdapter,
        kb_storage_repository: ITableMedatadaKBStorageRepository
    ):
        self.logger = setup_logger(__name__)
        self.__kb_retrieval_adapter = kb_retrieval_adapter
        self.__kb_storage_repository = kb_storage_repository

    def execute(self, input_dto: CreateTablesMetadataKBInputDTO) -> CreateTablesMetadataKBOutputDTO:
        """
        Execute the use case to create metadata knowledge base.

        :param input_dto: input object containing the tables list and credentials.
        :return: List of TableMetadataKBOutputContent objects containing metadata for each table.
        """

        # Building a TableMetadataKBRequest object
        kb_request = TableMetadataKBRequest(
            kb_id=str(uuid4()),
            kb_input_refence=input_dto.tables_list,
            datetime_creation=datetime.now(timezone.utc)
        )

        # Extracting info for logging purposes
        kb_id = kb_request.kb_id
        total_tables = len(input_dto.tables_list)

        self.logger.info(f"Building a KB {kb_id} using metadata from {total_tables} tables in the list")
        kb_output_content = self.__kb_retrieval_adapter.get_knowledge_base(
            kb_request=kb_request,
            account_credentials=input_dto.account_credentials
        )

        self.logger.info("Storing metadata in the storage repository for further access")
        self.__kb_storage_repository.store_knowledge_base(
            kb_request=kb_request,
            kb_output_content=kb_output_content
        )
        self.logger.info("Successfully retrieved and stored the KB")

        # Building the output DTO
        output_dto = CreateTablesMetadataKBOutputDTO(
            status_code=200,
            body={
                "kb_id": kb_request.kb_id
            }
        )

        return output_dto
