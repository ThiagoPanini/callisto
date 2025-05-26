import json

from app.src.features.create_tables_metadata_kb.presentation import create_metadata_kb_presentation
from app.src.features.process_user_prompt.presentation import process_user_prompt_presentation

from app.tests.mocks.mocked_input_events import (
    CREATE_KNOWLEDGE_BASE_INPUT_EVENT,
    PROCESS_USER_PROMPT_INPUT_EVENT
)


# Building Lambda handlers
create_metadata_kb_handler = create_metadata_kb_presentation.handler
process_user_prompt_handler = process_user_prompt_presentation.handler


"""
FEATURE: Create Knowledge Base

DESCRIPTION:
    This feature retrieves metadata from a list of tables using a data catalog adapter
    and stores it in an storage service for further access.
"""

response = create_metadata_kb_handler(
    event=CREATE_KNOWLEDGE_BASE_INPUT_EVENT,
    context=None
)
kb_id = json.loads(response["body"])["kb_id"]


"""
FEATURE: Process User Prompt

DESCRIPTION:
    This feature processes a user prompt by retrieving relevant information from a knowledge base
    and generating a response using a language model.
"""

# Changing information from input event based on previous features
input_body = json.loads(PROCESS_USER_PROMPT_INPUT_EVENT["body"])
input_body["kb_id"] = kb_id
PROCESS_USER_PROMPT_INPUT_EVENT["body"] = json.dumps(input_body)

"""
response = process_user_prompt_handler(
    event=PROCESS_USER_PROMPT_INPUT_EVENT,
    context=None
)
"""

# [TEMP]
from pydantic_ai import Agent
from pydantic import BaseModel
from typing import Optional



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

# Defining a structured output for the SQL agent
class SQLAgentOutput(BaseModel):
    plan_to_build_query: list[str]
    query_string: str
    possible_insights: Optional[str]


# Defining an SQL agent using PydanticAI
sql_agent = Agent(
    model="openai:gpt-4",
    system_prompt=(SQL_AGENT_SYSTEM_PROMPT),
    output_type=SQLAgentOutput,
)


# Defining a tool to retrieve the knowledge base
@sql_agent.tool_plain
def retrieve_knowledge_base():
    """
    Tool para retornar metadados de tabelas e colunas utilizados como base de conhecimento
    para que o agente especialista em SQL crie consultas com base nos pedidos dos usuários.

    :return: Metadados de tabelas e colunas.
    """

    r = process_user_prompt_handler(
        event=PROCESS_USER_PROMPT_INPUT_EVENT,
        context=None
    )

    return json.loads(r["body"])["kb"]


# Running the agent
response = sql_agent.run_sync(
    user_prompt="Quais análises eu posso fazer com esses dados?",
)

# print(response)
print(response.output.__dict__)
