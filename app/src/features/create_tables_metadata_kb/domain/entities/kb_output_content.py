from dataclasses import dataclass
from typing import Optional


@dataclass
class ColumnMetadata:
    """
    Class representing metadata for a column in a table.
    """
    column_name: str
    column_type: str
    column_description: str
    is_primary_key: Optional[bool] = False
    is_partition_key: Optional[bool] = False


@dataclass
class TableMetadataKBOutputContent:
    """
    Class representing metadata of a table in a database.
    """
    database_name: str
    table_name: str
    table_description: str
    table_columns: list[ColumnMetadata]


    def to_dict(self) -> dict:
        """
        Convert the KnowledgeBaseContent object to a dictionary.
        """
        return {
            **self.__dict__,
            "table_columns": [col.__dict__ for col in self.table_columns]
        }
