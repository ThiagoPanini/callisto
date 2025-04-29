import boto3

from app.src.features.get_tables_metadata.domain.interfaces.catalog_interface import (
    ICatalogInterface
)
from app.src.features.get_tables_metadata.domain.entities.table_metadata import TableMetadata
from app.src.features.get_tables_metadata.domain.entities.table_reference import TableReference
from app.src.features.get_tables_metadata.domain.entities.column_metadata import ColumnMetadata


class GlueCatalogAdapter(ICatalogInterface):
    def __init__(self, session: boto3.Session):
        self.__client = session.client("glue")
        self.__paginator = self.__client.get_paginator("get_tables")


    def get_table_metadata(self, tables_list: list[TableReference]) -> list[TableMetadata]:
        """
        Get metadata for a list of tables.

        :param tables_list: List of TableReference objects representing the tables.
        :return: List of TableMetadata objects containing metadata for each table.
        """

        # Tentar chamar método privado para criação de client e session
        # Passar credenciais no método do contrato (ruim, porém funciona)

        table_metadata_list = []

        for table_reference in tables_list:
            database_name = table_reference.database_name
            table_name = table_reference.table_name

            # Use paginator to handle large number of tables
            response_iterator = self.__paginator.paginate(
                DatabaseName=database_name,
                Expression=table_name
            )

            for page in response_iterator:
                for table in page["TableList"]:
                    columns = [
                        ColumnMetadata(
                            column_name=col["Name"],
                            column_type=col["Type"],
                            column_description=col.get("Comment", "")
                        )
                        for col in table["StorageDescriptor"]["Columns"]
                    ]

                    table_metadata = TableMetadata(
                        database_name=database_name,
                        table_name=table["Name"],
                        table_description=table.get("Description", ""),
                        table_columns=columns
                    )

                    table_metadata_list.append(table_metadata)

        return table_metadata_list
