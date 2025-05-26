from dataclasses import dataclass

from app.src.features.cross.utils.logger import setup_logger
from app.src.features.process_user_prompt.infra.repositories.s3_kb_retrieval_repository import (
    S3KBRetrievalRepository
)


@dataclass
class Dependencies:
    """
    Class representing the dependencies for Pydantic AI tools and agents.
    """
    logger = setup_logger(__name__)
    kb_retrieval_repository: S3KBRetrievalRepository
