from dataclasses import dataclass


@dataclass
class AccountCredentials:
    """
    Class representing credentials for a cloud provider account.
    """
    access_key_id: str
    secret_access_key: str
    session_token: str
