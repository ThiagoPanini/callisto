from dataclasses import dataclass

from app.src.features.cross.domain.entities.credentials import AccountCredentials


@dataclass
class ProcessUserPromptInputDTO:
    """
    Class representing the input data transfer object (DTO) for the use case.
    """
    user_prompt: str
    kb_id: str
    account_credentials: AccountCredentials
