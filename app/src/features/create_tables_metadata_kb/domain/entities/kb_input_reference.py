from dataclasses import dataclass


@dataclass
class TableMetadataKBInputReference:
    """
    Class representing a reference to a table in a database.
    """
    database_name: str
    table_name: str
