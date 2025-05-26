from typing import Optional
from enum import Enum

from pydantic import BaseModel

from app.src.features.process_user_prompt.ai.agents.generic.output import GenericDataAgentOutput
from app.src.features.process_user_prompt.ai.agents.sql.output import SQLAgentOutput


class AvailableAgents(Enum):
    """
    Class representing the available agents in the system.
    """
    GENERIC: str = "generic_agent"
    SQL: str = "sql_agent"
    VIZ: str = "viz_agent"


class AvailableAgentsOutput(BaseModel):
    generic: Optional[GenericDataAgentOutput]
    sql: Optional[SQLAgentOutput]


class MainAgentOutput(BaseModel):
    """
    Class representing the output of the Main Agent.
    """
    just_a_kind_comment_letting_user_know_the_answer_is_below: str
    agents_called_in_the_process: list[AvailableAgents]
    agents_output: AvailableAgentsOutput
