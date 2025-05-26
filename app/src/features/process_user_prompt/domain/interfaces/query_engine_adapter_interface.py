from abc import ABC, abstractmethod
from pandas import DataFrame
from typing import Optional

from app.src.features.cross.domain.entities.credentials import AccountCredentials


class IQueryEngineAdapter(ABC):
    """
    Interface for a query engine adapter.
    This interface defines the methods that a query engine adapter should implement.
    """

    @abstractmethod
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
