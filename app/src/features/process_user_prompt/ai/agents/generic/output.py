from pydantic import BaseModel

from app.src.features.process_user_prompt.ai.agents.generic.value_entity import (
    GenericAgentOutputEstimatedValue
)


class GenericDataAgentOutput(BaseModel):
    response_for_users_generic_questions: str
    estimated_value: GenericAgentOutputEstimatedValue
