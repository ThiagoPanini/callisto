from dataclasses import dataclass

from app.src.features.cross.utils.logger import setup_logger
from app.src.features.get_tables_metadata.domain.dtos.input_dto import InputDto
from app.src.features.get_tables_metadata.domain.interfaces.catalog_interface import (
    ICatalogInterface
)
from app.src.features.get_tables_metadata.domain.interfaces.cloud_provider_session_adapter import (
    ICloudProviderSessionAdapter
)


class GetTablesMetadataUseCase:
    """
    Use case for retrieving metadata of tables from a cloud provider.
    """

    def __init__(
        self,
        cloud_provider_session_adapter: ICloudProviderSessionAdapter,
        catalog_interface: ICatalogInterface
    ):
        self.__cloud_provider_session_adapter = cloud_provider_session_adapter
        self.__catalog_interface = catalog_interface
        self.logger = setup_logger(__name__)


    def execute(self, input_dto: InputDto) -> list[dict]:
        """
        Execute the use case to retrieve table metadata.

        :param input_dto: InputDto object containing the tables list and credentials.
        :return: List of dictionaries containing table metadata.
        """

        self.logger.info("Creating a session with user credentials")
        session = self.__cloud_provider_session_adapter.create_session(
            input_dto.credentials
        )


