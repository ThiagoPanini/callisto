from dataclasses import dataclass

@dataclass
class GenericAgentOutputEstimatedValue:
    """
    This class represents the estimated value of the Generic agent's response.
    It includes the estimated time to give the answer and a description of the reasoning behind
    that estimate.
    """
    estimated_hours_to_give_generic_response: float
    complexity_analysis: str
