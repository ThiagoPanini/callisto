from abc import ABC, abstractmethod

from app.src.features.get_tables_metadata.domain.entities.table_metadata import TableMetadata
from app.src.features.get_tables_metadata.domain.entities.table_reference import TableReference


class ICatalogInterface(ABC):

    @abstractmethod
    def get_table_metadata(self, tables_list: list[TableReference]) -> list[TableMetadata]:
        """
        Get metadata for a list of tables.

        :param tables_list: List of TableReference objects representing the tables.
        :return: List of TableMetadata objects containing metadata for each table.
        """
