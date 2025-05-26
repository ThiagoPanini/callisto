from dataclasses import dataclass

@dataclass
class SQLAgentOutputEstimatedValue:
    """
    This class represents the estimated value of the SQL agent's response.
    It includes the estimated time to build the SQL query and a description of the reasoning behind
    that estimate.
    """
    estimated_hours_to_build_sql_query: float
    complexity_analysis: str
