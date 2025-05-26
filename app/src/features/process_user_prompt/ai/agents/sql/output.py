from typing import Any, Optional

from pydantic import BaseModel

from app.src.features.process_user_prompt.ai.agents.sql.value_entity import (
    SQLAgentOutputEstimatedValue
)


class SQLAgentOutput(BaseModel):
    """
    Structured output for the SQL agent.
    """
    plan_to_build_query: list[str]
    query_string: str
    query_result: list[dict[str, Any]]
    possible_insights: Optional[str]
    estimated_value: SQLAgentOutputEstimatedValue
