from uuid import uuid4
from datetime import datetime, timezone

from app.src.features.cross.utils.logger import setup_logger
from app.src.features.process_user_prompt.domain.interfaces.kb_retrieval_repository_interface import (
    IKBRetrievalRepository
)
from app.src.features.process_user_prompt.domain.interfaces.query_engine_adapter_interface import (
    IQueryEngineAdapter
)
from app.src.features.process_user_prompt.domain.dtos.input_dto import ProcessUserPromptInputDTO
from app.src.features.process_user_prompt.domain.dtos.output_dto import ProcessUserPromptOutputDTO
from app.src.features.process_user_prompt.domain.entities.prompt_request import PromptRequest

from app.src.features.process_user_prompt.ai.core.dependencies import AIFrameworkDependencies
from app.src.features.process_user_prompt.ai.agents.main.agent import MainAgent


class ProcessUserPromptUseCase:
    """
    Use case for processing a user prompt.
    """

    def __init__(
        self,
        kb_retrieval_repository: IKBRetrievalRepository,
        query_engine_adapter: IQueryEngineAdapter
    ):
        self.logger = setup_logger(__name__)
        self.__kb_retrieval_repository = kb_retrieval_repository
        self.__query_engine_adapter = query_engine_adapter

    def execute(self, input_dto: ProcessUserPromptInputDTO) -> dict[str, str]:
        """
        Execute the use case to process a user prompt.

        :param input_dto: InputDto object containing the user prompt and knowledge base ID.
        :return: Processed response as a dictionary.
        """

        # Building a ProcessPromptRequest object
        prompt_request = PromptRequest(
            prompt_id=uuid4(),
            user_prompt=input_dto.user_prompt,
            kb_id=input_dto.kb_id,
            datetime_creation=datetime.now(timezone.utc)
        )

        # Initializing agents and tools dependencies
        dependencies = AIFrameworkDependencies(
            logger=self.logger,
            prompt_request=prompt_request,
            kb_retrieval_repository=self.__kb_retrieval_repository,
            query_engine_adapter=self.__query_engine_adapter,
            account_credentials=input_dto.account_credentials
        )

        # Retrieving the agent
        main_agent = MainAgent.get_agent()

        # Running the agent
        self.logger.info("Running the Main Agent in synchronous mode")
        response = main_agent.run_sync(
            user_prompt=prompt_request.user_prompt,
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

"""
Ideas:
- Main agent
- Tools that call other agents (SQL, Viz, Spark, Diagnostic, Optimizer)
"""