from typing import Any, Type

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.tools import Tool

from app.src.features.process_user_prompt.ai.agents.sql.output import SQLAgentOutput
from app.src.features.process_user_prompt.ai.core.dependencies import AIFrameworkDependencies
from app.src.features.process_user_prompt.ai.core.tools import (
    retrieve_table_metadata_kb,
    get_dataframe_from_sql_query
)


# Defining the prompt for the SQL agent
SQL_AGENT_SYSTEM_PROMPT: str = """
<role>
    You are an expert SQL agent specialized in querying and analyzing data using Amazon Athena.
    Your primary objective is to generate efficient, accurate, and well-structured SQL queries
    in response to user questions, using only the available or retrieved table and column metadata.
</role>

<context>
    Users interact with you to gain business insights from their data through SQL queries.
    Each interaction consists of:
    - (1) a business question or analytical request in natural language, and
    - (2) a list of tables from a catalog for which metadata must be retrieved using function tools.
    The provided metadata is essential for you to interpret the user's request and generate relevant
    SQL queries.
</context>

<instructions>
    - Receive a business question and a list of tables that may or may not contain the required
      information.
    - Retrieve the metadata for the specified tables using available function tools.
    - Carefully analyze the question and the metadata to identify all relevant tables, columns,
      and business logic needed to answer.
    - If there is any ambiguity in mapping business terms to metadata, or if information is missing,
      ask the user for clarification before generating a query.
    - If the question is too broad, suggest specific analyses or queries that can be performed with
      the available data.
    - When appropriate, generate an Amazon Athena/Trino-compatible SQL query that answers the user's
      question.
</instructions>

<rules>
    - Always answer in brazilian portuguese
    - Only generate SELECT queries; never perform data modification (INSERT, UPDATE, DELETE).
    - Use only SQL syntax compatible with Amazon Athena (Presto/Trino).
    - For GROUP BY, always use the full calculation, never a column alias.
    - Always filter by explicit partitions when possible to optimize performance.
    - Only use tables and columns present in the provided metadata; do not assume the existence of
      other data.
    - Use LIMIT in queries that do not perform aggregation.
    - Do NOT include comments within the SQL query string.
    - All explanations and reasoning should be outside the SQL string (never as SQL comments).
    - If the user's request cannot be answered with SQL given the metadata, ask for more context
      and suggest specific analyses that can be performed with the available data.
</rules>

<output>
    - Consider the SQLAgentOutput BaseModel class
    - For the plan_to_build_query attribute, you need to describe all the steps you have planed to
      build the SQL query in the first person plural. Use sentences like "We should take a look",
      "We need to get informations from table", "We need to join", and so on.
</output>
"""

# Defining the agent
class SQLAgent:
    """
    Factory class for creating and configuring an Agent instance
    optimized for SQL query generation using Amazon Athena.
    """

    @classmethod
    def get_agent(
        cls,
        model: str = "openai:gpt-4o",
        system_prompt: str = SQL_AGENT_SYSTEM_PROMPT,
        deps_type: Any = AIFrameworkDependencies,
        output_type: Type[BaseModel] = SQLAgentOutput,
        tools: list[Tool] = [
            Tool(
                function=retrieve_table_metadata_kb,
                name=retrieve_table_metadata_kb.__name__,
                description=retrieve_table_metadata_kb.__doc__,
                takes_ctx=True,
                max_retries=1,
            ),
            Tool(
                function=get_dataframe_from_sql_query,
                name=get_dataframe_from_sql_query.__name__,
                description=get_dataframe_from_sql_query.__doc__,
                takes_ctx=True,
                max_retries=1,
            )
        ]
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
    def get_and_run_sql_agent(ctx: RunContext[AIFrameworkDependencies]) -> SQLAgentOutput:
        """
        Call the SQL agent to answer user requests that can be fulfilled with a SQL query.

        This function is designed to be used by the main supervisor agent whenever a user's business 
        question or analytics request can be addressed by querying data with SQL. It retrieves the user's 
        prompt and relevant dependencies from the execution context, invokes the specialized SQL agent to 
        analyze the request, generate an efficient and valid SQL query based on available table and
        column metadata, and executes the query to obtain results. The output includes the generated SQL
        query, the agent's reasoning, and the query results, encapsulated in an SQLAgentOutput object.

        Use this tool when the user's request involves retrieving, aggregating, or analyzing data that
        can be expressed as a SQL SELECT statement.

        At the end, use the SQLAgentOutputEstimatedValue class to guide you to give a estimated value
        of your response so users can get an idea of how much time they are saving by using the agent.

        :param ctx: The execution context containing user input, dependencies, and logging.
        :return: An SQLAgentOutput object containing the SQL query, reasoning, and results.
        """

        # Retrieving the logger object from the context
        logger = ctx.deps.logger

        # Retrieving the agent
        sql_agent = SQLAgent.get_agent()
        logger.info("Running the SQL Agent in synchronous mode")

        return sql_agent.run_sync(
            user_prompt=ctx.deps.prompt_request.user_prompt,
            deps=ctx.deps
        )
