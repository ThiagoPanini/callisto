from abc import ABC, abstractmethod
from typing import Any

from app.src.features.get_tables_metadata.domain.entities.credentials import AccountCredentials


class ICloudProviderSessionAdapter(ABC):

    @abstractmethod
    def create_session(self, credentials: AccountCredentials) -> Any:
        """
        Create a session with the cloud provider using the provided credentials.

        :param credentials: AccountCredentials object containing the credentials.
        :return: A session object for interacting with the cloud provider.
        """
