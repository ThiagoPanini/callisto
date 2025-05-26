from uuid import uuid4
import json
from datetime import datetime, timezone

from app.src.features.cross.utils.logger import setup_logger
from app.src.features.process_user_prompt.domain.entities.prompt_request import PromptRequest
from app.src.features.process_user_prompt.domain.interfaces.kb_retrieval_repository_interface import (
    IKBRetrievalRepository
)
from app.src.features.process_user_prompt.domain.interfaces.query_engine_adapter_interface import (
    IQueryEngineAdapter
)
from app.src.features.process_user_prompt.domain.dtos.input_dto import ProcessUserPromptInputDTO
from app.src.features.process_user_prompt.domain.dtos.output_dto import ProcessUserPromptOutputDTO

# [TMP]
from dataclasses import dataclass
import logging
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from typing import Any, Optional
from pandas import DataFrame


# Defining dependencies for the agents and tools to run
@dataclass
class Dependencies:
    logger: logging.Logger
    prompt_request: PromptRequest
    kb_retrieval_repository: IKBRetrievalRepository
    query_engine_adapter: IQueryEngineAdapter


# Defining a structured output for the SQL agent
class SQLAgentOutput(BaseModel):
    plan_to_build_query: list[str]
    query_string: str
    query_result: dict[str, Any]
    possible_insights: Optional[str]


# Defining a prompt for the SQL agent
SQL_AGENT_SYSTEM_PROMPT: str = """
<role>
Agente especialista em SQL para consulta e análise de dados no Amazon Athena, com foco em
gerar queries eficientes e precisas com base em perguntas em linguagem natural e metadados
de tabelas previamente disponíveis ou resgatadas através de tools.
</role>

<context>
O agente será utilizado por usuários que desejam obter insights de dados através de consultas SQL.
Nesse cenário, os usuários irão fornecer perguntas analíticas e uma base de conhecimento que
se materializa em metadados de tabelas e colunas previamente extraídos e resgatados. Essa base
de conhecimento é fundamental para que o agente possa interpretar o pedido do usuário e gerar
queries SQL condizentes com os dados disponíveis.
</context>

<instructions>
- Receba uma pergunta em linguagem natural ou um objetivo analítico.
- Receba ou obtenha os metadados das tabelas previamente informadas.
- Analise a pergunta e identifique as tabelas e atributos relevantes para o contexto solicitado.
- Gere uma query SQL compatível com o Athena, incluindo filtros, joins e partições relevantes.
- Quando apropriado, proponha otimizações para reduzir o custo da consulta.
- Certifique-se de que a query seja legível e bem estruturada.
- Inclua comentários explicativos quando necessário.
- Quando aplicável, utilize funções nativas do Athena para manipulação de dados, como date_parse,
    json_extract, unnest, regexp_extract, entre outras.
</instructions>

<rules>
- Utilize apenas sintaxe SQL compatível com o Amazon Athena (Presto/Trino).
- Quando utilizar GROUP BY, jamais inclua o alias das colunas calculadas, mas sim o cálculo em si
- Sempre que possível, filtre por partições explícitas para otimizar performance.
- Não faça suposições sobre nomes de tabelas inexistentes; solicite mais contexto caso necessário.
- Use LIMIT nas consultas quando nenhuma agregação for solicitada.
- Nunca modifique, insira ou delete dados — apenas leitura (SELECT).
- Não inclua comentários na string de query SQL para evitar problemas de execução.
</rules>

<output>
- A saída deve ser estruturada e seguir o modelo BaseModel definido na classe SQLAgentOutput.
</output>

<tools>
- retrieve_knowledge_base: Tool para resgatar metadados de tabelas e colunas.
</tools>

<guardrails>
- Você deve apenas responder perguntas que possam ser respondidas com SQL.
- Se a pergunta não puder ser respondida com SQL, informe que não é possível responder.
- Se o pedido do usuário for genérico, sugira análises específicas que podem ser feitas com os dados.
</guardrails>
"""



class ProcessUserPromptUseCase:
    """
    Use case for processing a user prompt.
    """

    def __init__(
        self,
        kb_retrieval_repository: IKBRetrievalRepository,
        query_engine_adapter: IQueryEngineAdapter,
        # agents_config: dict[str, AgentConfig]
    ):
        self.logger = setup_logger(__name__)
        self.__kb_retrieval_repository = kb_retrieval_repository
        self.__query_engine_adapter = query_engine_adapter
        # self.__agents_config = agents_config

    def execute(self, input_dto: ProcessUserPromptInputDTO) -> dict[str, str]:
        """
        Execute the use case to process a user prompt.

        :param input_dto: InputDto object containing the user prompt and knowledge base ID.
        :return: Processed response as a dictionary.
        """

        # Building a ProcessPromptRequest object
        prompt_request = PromptRequest(
            prompt_id=uuid4(),
            prompt_content=input_dto.prompt_content,
            kb_id=input_dto.kb_id,
            created_at=datetime.now(timezone.utc),
            account_credentials=input_dto.account_credentials
        )

        # Initializing agents and tools dependencies
        dependencies = Dependencies(
            logger=self.logger,
            prompt_request=prompt_request,
            kb_retrieval_repository=self.__kb_retrieval_repository,
            query_engine_adapter=self.__query_engine_adapter
        )

        # Defining a SQL agent
        sql_agent = Agent(
            model="openai:gpt-4",
            system_prompt=(SQL_AGENT_SYSTEM_PROMPT),
            deps_type=Dependencies,
            output_type=SQLAgentOutput,
        )

        # Defining a tool to retrieve the knowledge base
        @sql_agent.tool
        def retrieve_knowledge_base(ctx: RunContext[Dependencies]) -> list[dict[str, Any]]:
            """
            Tool para retornar metadados de tabelas e colunas utilizados como base de conhecimento
            para que o agente especialista em SQL crie consultas com base nos pedidos dos usuários.

            :return: Metadados de tabelas e colunas.
            """

            # Defining the adapter to retrieve the knowledge base
            kb = ctx.deps.kb_retrieval_repository.retrieve_knowledge_base(
                kb_id=ctx.deps.prompt_request.kb_id
            )

            return kb

        @sql_agent.tool
        def run_query(ctx: RunContext[Dependencies], query_string: str) -> list[dict[str, Any]]:
            """
            Tool para executar uma query SQL gerada pelo agente especialista em SQL
            após receber o pedido do usuário, retornar os metadados das tabelas disponíveis
            e acionar um modelo de LLM para gerar uma query SQL.

            :param ctx: objeto de contexto contendo as dependências da solução.
            :param query_string: Query SQL gerada pelo próprio agente.
            :return: Result of the SQL query as a list of dictionaries.
            """

            # Retrieving the logger oibject from the context
            logger = ctx.deps.logger

            # Running the SQL query using the provided adapter
            logger.info(f"Retrieving KB {input_dto.kb_id} from repository")
            df = ctx.deps.query_engine_adapter.run_query(
                query_string=query_string,
                account_credentials=ctx.deps.prompt_request.account_credentials
            )

            return df.to_dict(orient="records")

        # Running the agent
        response = sql_agent.run_sync(
            user_prompt="Qual o total de pedidos para cada estado?",
            deps=dependencies
        )

        # Building the output DTO
        output_dto = ProcessUserPromptOutputDTO(
            status_code=200,
            body={
                "response": response.output.__dict__
            }
        )

        return output_dto
