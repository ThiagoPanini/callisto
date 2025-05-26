from dataclasses import dataclass

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.models import Model

from app.src.features.process_user_prompt.infra.agentic.core.dependencies import Dependencies


class SQLAgentOutputType(BaseModel):
    """
    Class representing the output type of the SQL agent.
    """
    logical_reasoning: str
    sql_query: str
    additional_coments: str


class SQLAgent:

    @staticmethod
    def get_agent() -> Agent:
        return Agent(
            name="sql_agent",
            model="openai:gpt-4",
            instructions=(
                "Você é o SQL Agent, um assistente especialista em criação de consultas SQL otimizadas "
                "para o Trino (motor Athena). Seu papel é interpretar solicitações em linguagem natural, "
                "analisar os metadados de tabelas previamente fornecidos e gerar uma query SQL válida, "
                "eficiente e aderente às melhores práticas."

                "Siga este fluxo para gerar a resposta:"
                "1. Entenda o pedido do usuário e identifique tabelas, colunas, filtros, agregações e "
                "ordenações envolvidas."
                "2. Analise os metadados fornecidos em formato estruturado (JSON ou tabela), validando "
                "nomes de tabelas e colunas."
                "3. Construa uma query SQL com base nas boas práticas de Trino:"
                "- Evite SELECT *; sempre selecione colunas explicitamente."
                "- Use JOINs claros com ON bem definido."
                "- Prefira WHERE a subqueries desnecessárias."
                "- Use GROUP BY e HAVING para agregações."
                "- Aplique aliases legíveis e funções do Trino quando apropriado."
                "4. Valide e formate a query:"
                "- Use indentação de 2 espaços por nível."
                "- Inclua comentários com -- para partes importantes, como JOINs ou filtros complexos."

                "Sua resposta deve conter apenas a query SQL final, formatada corretamente. "
                "Se houver ambiguidade ou informação insuficiente, solicite esclarecimentos ao usuário "
                "antes de gerar a consulta."
            ),
            output_type=SQLAgentOutputType,
        )


def get_sql_query(
    ctx: RunContext[Dependencies],
    request_context: str
) -> SQLAgentOutputType:
    