from dataclasses import dataclass
from datetime import datetime

from app.src.features.cross.domain.value_objects import ProcessingStatus


@dataclass
class PromptRequest:
    """
    Class representing a request for processing a user prompt.
    """
    prompt_id: str
    user_prompt: str
    kb_id: str
    datetime_creation: datetime
    datetime_last_update: datetime = None
    status: ProcessingStatus = ProcessingStatus.PENDING
