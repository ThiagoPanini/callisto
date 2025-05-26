import os
from typing import Optional

import boto3
from pandas import DataFrame
from pyathena import connect
from pyathena.pandas.util import as_pandas

from app.src.features.process_user_prompt.domain.interfaces.query_engine_adapter_interface import (
    IQueryEngineAdapter
)
from app.src.features.cross.domain.entities.credentials import AccountCredentials


class AthenaQueryEngineAdapter(IQueryEngineAdapter):
    """
    Adapter for running queries against Amazon Athena.
    """

    def __get_s3_staging_dir(self, account_credentials: AccountCredentials) -> str:
        """
        Get the S3 bucket name for staging queries.

        :return: The S3 bucket name for staging queries.
        """

        # Getting a boto3 sts client using the provided AWS account credentials to get the account ID
        session = boto3.session.Session(
            aws_access_key_id=account_credentials.access_key_id,
            aws_secret_access_key=account_credentials.secret_access_key,
            region_name=os.getenv("AWS_REGION"),
        )
        sts_client = session.client("sts")
        account_id = sts_client.get_caller_identity()["Account"]

        # Constructing the S3 bucket name and folder prefix using environment variables
        bucket_prefix = os.getenv('ATHENA_QUERY_OUTPUT_S3_BUCKET_NAME_PREFIX')
        bucket_name = f"{bucket_prefix}-{account_id}-{os.getenv('AWS_REGION')}"
        folder_prefix = os.getenv("ATHENA_QUERY_OUTPUT_S3_FOLDER_PREFIX")

        return f"s3://{bucket_name}/{folder_prefix}"


    def __get_connection(self, account_credentials: AccountCredentials):
        return connect(
            aws_access_key_id=account_credentials.access_key_id,
            aws_secret_access_key=account_credentials.secret_access_key,
            s3_staging_dir=self.__get_s3_staging_dir(account_credentials=account_credentials),
            region_name=os.getenv("AWS_REGION"),
        )


    def run_query(
        self,
        query_string: str,
        account_credentials: Optional[AccountCredentials]
    ) -> DataFrame:
        """
        Run a query against the query engine.

        :param query_string: The SQL query string to be executed.
        :param account_credentials: Optional AWS account credentials for authentication.

        :return: The result of the query as a pandas DataFrame.
        """

        # Getting a pyathena connection object using the provided AWS account credentials
        conn = self.__get_connection(account_credentials=account_credentials)

        # Running the query and returning the result as a pandas DataFrame
        with conn.cursor() as cursor:
            cursor.execute(query_string)
            return as_pandas(cursor)
