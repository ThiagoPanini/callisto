from dataclasses import dataclass
import logging

from app.src.features.process_user_prompt.domain.entities.prompt_request import PromptRequest
from app.src.features.process_user_prompt.domain.interfaces.kb_retrieval_repository_interface import (
    IKBRetrievalRepository
)
from app.src.features.process_user_prompt.domain.interfaces.query_engine_adapter_interface import (
    IQueryEngineAdapter
)
from app.src.features.cross.domain.entities.credentials import AccountCredentials


@dataclass
class AIFrameworkDependencies:
    """
    Class representing the dependencies required for the AI framework.
    """
    logger: logging.Logger
    prompt_request: PromptRequest
    kb_retrieval_repository: IKBRetrievalRepository
    query_engine_adapter: IQueryEngineAdapter
    account_credentials: AccountCredentials
