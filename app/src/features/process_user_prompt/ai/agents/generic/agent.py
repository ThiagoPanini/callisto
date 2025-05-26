from typing import Any, Type

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.tools import Tool

from app.src.features.process_user_prompt.ai.agents.generic.output import GenericDataAgentOutput
from app.src.features.process_user_prompt.ai.core.dependencies import AIFrameworkDependencies


# Defining the prompt for the agent
GENERIC_DATA_AGENT_SYSTEM_PROMPT: str = """
<role>
    You are a generic data agent designed to assist users with any requests that do not fit into a 
    specific step of the data analytics journey. Your primary objective is to provide helpful, accurate, 
    and clear answers to general questions while actively guiding users toward formulating business-focused 
    questions that can drive actionable data analyses and insights.
</role>

<context>
    Users may ask you a broad range of questions, including general inquiries, non-technical topics, 
    clarifications about data concepts, or requests that lack clear business or analytical objectives.
    You act as a flexible resource for handling these requests, providing value through information, 
    explanation, or redirection. However, your core value lies in encouraging users to reframe their 
    queries into business questions that can be addressed through data analytics tools or workflows.
</context>

<instructions>
    - Receive and comprehend the user's request, regardless of its specificity or relevance to data analytics.
    - Provide clear, concise, and accurate answers to general questions within your knowledge scope.
    - Whenever possible, identify opportunities to reframe or redirect the user's inquiry into a 
      business-focused question that could benefit from data-driven analysis.
    - If the user's request is vague or not actionable, suggest ways to clarify or narrow it into a 
      question that aligns with business needs or can be addressed by specialized data agents or tools.
    - Offer examples of how requests can be transformed into business questions relevant to data analytics.
    - Maintain a supportive and educational tone, empowering users to get the most value from data analytics.
    - If the request contains any ambiguity, ask relevant follow-up questions to clarify the user's intent 
      and help them focus on actionable outcomes.
</instructions>

<rules>
    - Always answer in brazilian portuguese
    - Always answer general questions to the best of your ability, but prioritize guiding users toward 
      business-oriented, actionable queries.
    - Never fabricate information or provide unsupported data.
    - Avoid technical jargon unless it is necessary and appropriate for the user's context.
    - Clearly communicate the value of transforming general inquiries into business questions suitable for 
      data analysis.
    - If a user's request cannot be reframed or answered meaningfully, explain why and suggest what the 
      user could provide or try next.
    - Maintain a user-friendly, approachable, and helpful tone in all responses.
</rules>
"""

# Defining the agent
class GenericDataAgent:
    """
    Factory class for creating and configuring an Agent instance designed for generic answers
    """

    @classmethod
    def get_agent(
        cls,
        model: str = "openai:gpt-4o",
        system_prompt: str = GENERIC_DATA_AGENT_SYSTEM_PROMPT,
        deps_type: Any = AIFrameworkDependencies,
        output_type: Type[BaseModel] = GenericDataAgentOutput,
        tools: list[Tool] = []
    ) -> Agent:
        """
        Instantiate and return a configured Agent instance.
        """
        return Agent(
            model=model,
            system_prompt=system_prompt,
            deps_type=deps_type,
            output_type=output_type,
            tools=tools,
        )

    @staticmethod
    def get_and_run_generic_agent(
        ctx: RunContext[AIFrameworkDependencies]
    ) -> GenericDataAgentOutput:
        """
        Call the generic data agent to handle user requests that do not fit into any specific
        step of the data analytics journey.

        This function is designed to be used by the main supervisor agent when a user's request
        is general, ambiguous, or unrelated to the core data analytics workflow (such as data
        discovery, querying, transformation, analysis, or visualization). It retrieves the user's
        request and relevant dependencies from the execution context, invokes the generic data agent
        to provide a helpful and accurate answer, and, whenever possible, guides the user toward
        formulating a business-focused question that can be addressed through data analytics.

        Use this tool when:
        - The user's request is outside the standard data analytics pipeline.
        - The request is general, conceptual, or not actionable with specialized data agents or
          tools.
        - The user needs clarification, education, or redirection to make their question more
          data-driven and business-oriented.

        :param ctx: The execution context containing user input, dependencies, and logging.
        :return: A GenericAgentOutput object containing the agent's response and suggestions for
        next steps.
        """

        # Retrieving the logger object from the context
        logger = ctx.deps.logger

        # Retrieving the agent
        generic_data_agent = GenericDataAgent.get_agent()
        logger.info("Running the Generic Agent in synchronous mode")

        return generic_data_agent.run_sync(
            user_prompt=ctx.deps.prompt_request.user_prompt,
            deps=ctx.deps
        )
