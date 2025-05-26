from enum import Enum


class ProcessingStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
    DELETED = "deleted"

    def __str__(self):
        return self.value
