from dataclasses import dataclass


@dataclass
class TableReference:
    """
    Class representing a reference to a table in a database.
    """
    database_name: str
    table_name: str
