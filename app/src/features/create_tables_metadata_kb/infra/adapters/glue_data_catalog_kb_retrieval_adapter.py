import os
from typing import Optional

import boto3
import boto3.session

from app.src.features.create_tables_metadata_kb.domain.interfaces.kb_retrieval_adapter_interface import (
    ITableMetadataKBRetrievalAdapter
)
from app.src.features.create_tables_metadata_kb.domain.entities.kb_request import TableMetadataKBRequest
from app.src.features.create_tables_metadata_kb.domain.entities.kb_output_content import (
    ColumnMetadata,
    TableMetadataKBOutputContent
)
from app.src.features.cross.domain.entities.credentials import AccountCredentials


class GlueDataCatalogKBRetrievalAdapter(ITableMetadataKBRetrievalAdapter):

    def __get_client_with_user_credentials(self, account_credentials: AccountCredentials):
        """
        Create a Glue client using the provided AWS account credentials

        :param account_credentials: AccountCredentials object containing AWS credentials.
        :return: Boto3 Glue client.
        """
        session = boto3.session.Session(
            aws_access_key_id=account_credentials.access_key_id,
            aws_secret_access_key=account_credentials.secret_access_key,
            aws_session_token=account_credentials.session_token,
            region_name=os.getenv("AWS_REGION"),
        )
        return session.client("glue")


    def get_knowledge_base(
        self,
        kb_request: TableMetadataKBRequest,
        account_credentials: AccountCredentials
    ) -> Optional[list[TableMetadataKBOutputContent]]:
        """
        Retrieve knowledge base from the repository.

        :param kb_request: TableMetadataKBRequest object to be retrieved.
        :param account_credentials: AccountCredentials object containing requester credentials.

        :return: List of TableMetadataKBOutputContent objects if found, None otherwise.
        """

        # Creating a Glue client using the provided AWS account credentials and a paginator
        client = self.__get_client_with_user_credentials(
            account_credentials=account_credentials
        )
        paginator = client.get_paginator("get_tables")

        kb_output_content = []
        for kb_input_reference in kb_request.kb_input_refence:
            database_name = kb_input_reference.database_name
            table_name = kb_input_reference.table_name

            # Use paginator to handle large number of tables
            response_iterator = paginator.paginate(
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

                    kb_content = TableMetadataKBOutputContent(
                        database_name=database_name,
                        table_name=table["Name"],
                        table_description=table.get("Description", ""),
                        table_columns=columns
                    )

                    kb_output_content.append(kb_content)

        return kb_output_content
