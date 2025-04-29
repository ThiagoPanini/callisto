from typing import Any
import boto3

from app.src.features.get_tables_metadata.domain.entities.credentials import AccountCredentials
from app.src.features.get_tables_metadata.domain.interfaces.cloud_provider_session_adapter import (
    ICloudProviderSessionAdapter
)


class AWSSessionAdapter(ICloudProviderSessionAdapter):
    """
    AWS session adapter for creating a session with AWS services.
    """

    def create_session(self, credentials: AccountCredentials) -> Any:
        """
        Create a session with AWS using the provided credentials.

        :param credentials: AccountCredentials object containing the credentials.
        :return: A session object for interacting with AWS services.
        """
        return boto3.Session(
            aws_access_key_id=credentials.access_key_id,
            aws_secret_access_key=credentials.secret_access_key,
            aws_session_token=credentials.session_token,
        )
