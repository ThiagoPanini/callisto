import json

from app.src.features.create_tables_metadata_kb.presentation import create_metadata_kb_presentation
from app.src.features.process_user_prompt.presentation import process_user_prompt_presentation

from app.tests.mocks.mocked_input_events import (
    CREATE_KNOWLEDGE_BASE_INPUT_EVENT,
    PROCESS_USER_PROMPT_INPUT_EVENT
)


# Building Lambda handlers
#create_metadata_kb_handler = create_metadata_kb_presentation.handler
process_user_prompt_handler = process_user_prompt_presentation.handler


"""
FEATURE: Create Knowledge Base

DESCRIPTION:
    This feature retrieves metadata from a list of tables using a data catalog adapter
    and stores it in an storage service for further access.
"""
"""
response = create_metadata_kb_handler(
    event=CREATE_KNOWLEDGE_BASE_INPUT_EVENT,
    context=None
)
kb_id = json.loads(response["body"])["kb_id"]
"""

"""
FEATURE: Process User Prompt

DESCRIPTION:
    This feature processes a user prompt by retrieving relevant information from a knowledge base
    and generating a response using a language model.
"""

# Changing information from input event based on previous features
# input_body = json.loads(PROCESS_USER_PROMPT_INPUT_EVENT["body"])
# input_body["kb_id"] = kb_id
# PROCESS_USER_PROMPT_INPUT_EVENT["body"] = json.dumps(input_body)

response = process_user_prompt_handler(
    event=PROCESS_USER_PROMPT_INPUT_EVENT,
    context=None
)

print(response)
