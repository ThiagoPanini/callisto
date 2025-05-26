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
            prompt_content=input_dto.prompt_content,
            kb_id=input_dto.kb_id,
            created_at=datetime.now(timezone.utc),
            account_credentials=input_dto.account_credentials
        )

        # Retrieve the knowledge base using the provided KB ID
        self.logger.info(f"Retrieving KB {input_dto.kb_id} from the repository")
        kb = self.__kb_retrieval_repository.retrieve_knowledge_base(
            kb_id=prompt_request.kb_id
        )
        approx_tokens = len(json.dumps(kb))
        self.logger.info(f"Succesfully retrieved KB with {approx_tokens} approximate tokens")

        # Running a SQL query against the query engine
        df = self.__query_engine_adapter.run_query(
            query_string="SELECT * FROM db_olist_ecommerce.tbl_olist_customers LIMIT 10",
            account_credentials=prompt_request.account_credentials
        )

        # Building the output DTO
        output_dto = ProcessUserPromptOutputDTO(
            status_code=200,
            body={
                "kb": kb,
                "df": df,
            }
        )

        return output_dto
