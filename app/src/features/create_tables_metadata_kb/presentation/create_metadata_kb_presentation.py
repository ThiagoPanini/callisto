import json
from typing import Any

from app.src.features.create_tables_metadata_kb.infra.mappers.lambda_mapper import LambdaMapper
from app.src.features.create_tables_metadata_kb.infra.adapters.glue_data_catalog_kb_retrieval_adapter import (
    GlueDataCatalogKBRetrievalAdapter
)
from app.src.features.create_tables_metadata_kb.infra.repositories.s3_kb_storage_repository import (
    S3KBStorageRepository
)

from app.src.features.create_tables_metadata_kb.usecases.create_metadata_kb_usecase import (
    CreateTablesMetadataKBUseCase
)


# Initializing mappers, adapters and repositories
lambda_mapper = LambdaMapper()
kb_retrieval_adapter = GlueDataCatalogKBRetrievalAdapter()
kb_storage_repository = S3KBStorageRepository()

# Initializing the use case
use_case = CreateTablesMetadataKBUseCase(
    kb_retrieval_adapter=kb_retrieval_adapter,
    kb_storage_repository=kb_storage_repository
)


# Define a handler function for AWS Lambda
def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """
    AWS Lambda handler function.

    :param event: The event data passed to the Lambda function.
    :param context: The context object provided by AWS Lambda.
    :return: A response dictionary containing the status code and body.
    """
    # Convert the Lambda event to a CreateMetadataKbInputDto
    input_dto = lambda_mapper.get_input_dto_from_lambda_event(event=event)

    # Execute the use case
    output_dto = use_case.execute(input_dto=input_dto)

    # Return a response
    return {
        "status_code": output_dto.status_code,
        "headers": output_dto.headers,
        "body": json.dumps(output_dto.body)
    }
