from typing import Any

from app.src.features.process_user_prompt.infra.mappers.lambda_mapper import LambdaMapper
from app.src.features.process_user_prompt.infra.repositories.s3_kb_retrieval_repository import (
    S3KBRetrievalRepository
)
from app.src.features.process_user_prompt.infra.adapters.athena_query_engine_adapter import (
    AthenaQueryEngineAdapter
)
from app.src.features.process_user_prompt.usecases.process_user_prompt_usecase_v4 import (
    ProcessUserPromptUseCase
)


# Initializing mappers, adapters and repositories
lambda_mapper = LambdaMapper()
kb_retrieval_repository = S3KBRetrievalRepository()
query_engine_adapter = AthenaQueryEngineAdapter()

# Initializing the use case
use_case = ProcessUserPromptUseCase(
    kb_retrieval_repository=kb_retrieval_repository,
    query_engine_adapter=query_engine_adapter
)


# Define a handler function for AWS Lambda
def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """
    AWS Lambda handler function.

    :param event: The event data passed to the Lambda function.
    :param context: The context object provided by AWS Lambda.
    :return: A response dictionary containing the status code and body.
    """
    # Convert the Lambda event to a ProcessUserPromptInputDto
    input_dto = lambda_mapper.get_input_dto_from_lambda_event(event=event)

    # Execute the use case
    output_dto = use_case.execute(input_dto=input_dto)

    # Return a response
    return {
        "status_code": output_dto.status_code,
        "headers": output_dto.headers,
        # "body": json.dumps(output_dto.body)
        "body": output_dto.body
    }
