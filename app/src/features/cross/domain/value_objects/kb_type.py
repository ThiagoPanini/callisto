from enum import Enum


class KBType(Enum):
    TABLE_METADATA = "table_metadata"
    DOCUMENTATION = "documentation"
    FAQ = "faq"
    PROCEDURE_MANUAL = "procedure_manual"
    CONVERSATION_LOGS = "conversation_logs"
    PRODUCT_CATALOG = "product_catalog"
    API_REFERENCE = "api_reference"
    FILE_INDEX = "file_index"
    DATA_DICTIONARY = "data_dictionary"
    CODE_SNIPPETS = "code_snippets"
    SYSTEM_ARCHITECTURE = "system_architecture"
    GLOSSARY = "glossary"
    LEGAL_DOCUMENTS = "legal_documents"

    def __str__(self):
        return self.value
