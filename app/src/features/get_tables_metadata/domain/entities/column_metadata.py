from dataclasses import dataclass


@dataclass
class ColumnMetadata:
    """
    Represents metadata for a column in a table.
    """
    column_name: str
    column_type: str
    column_description: str
    is_primary_key: bool = False
    is_partition_key: bool = False
