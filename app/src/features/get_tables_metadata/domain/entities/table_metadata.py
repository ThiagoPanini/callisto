from dataclasses import dataclass
from app.src.features.get_tables_metadata.domain.entities.column_metadata import ColumnMetadata


@dataclass
class TableMetadata:
    """
    Class representing metadata of a table in a database.
    """
    database_name: str
    table_name: str
    table_description: str
    table_columns: list[ColumnMetadata]


    def to_dict(self) -> dict:
        """
        Convert the TableMetadata object to a dictionary.
        """
        return {
            **self.__dict__,
            "table_columns": [col.to_dict() for col in self.table_columns]
        }
