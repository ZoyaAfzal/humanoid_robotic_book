from pydantic import BaseModel
from typing import Optional, Dict, Any
from enum import Enum


class ErrorCode(str, Enum):
    """
    Enum for error codes used in the application
    """
    INVALID_QUERY = "INVALID_QUERY"
    INSUFFICIENT_CONTEXT = "INSUFFICIENT_CONTEXT"
    RETRIEVAL_ERROR = "RETRIEVAL_ERROR"
    AGENT_ERROR = "AGENT_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class APIError(Exception):
    """
    Base exception class for API errors
    """
    def __init__(self, error_code: ErrorCode, message: str, details: Optional[Dict[str, Any]] = None):
        self.error_code = error_code
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(APIError):
    """
    Exception raised for validation errors
    """
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorCode.VALIDATION_ERROR, message, details)


class InsufficientContextError(APIError):
    """
    Exception raised when there's insufficient context to answer a query
    """
    def __init__(self, message: str = "Unable to generate answer: no relevant content found for the given query", details: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorCode.INSUFFICIENT_CONTEXT, message, details)


class RetrievalError(APIError):
    """
    Exception raised for retrieval-related errors
    """
    def __init__(self, message: str = "Error occurred during content retrieval", details: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorCode.RETRIEVAL_ERROR, message, details)


class AgentError(APIError):
    """
    Exception raised for agent-related errors
    """
    def __init__(self, message: str = "Error occurred during agent processing", details: Optional[Dict[str, Any]] = None):
        super().__init__(ErrorCode.AGENT_ERROR, message, details)