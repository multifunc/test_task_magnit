from http.client import responses
from typing import Optional

from core import statuses


class HTTPException(Exception):
    """
    Базовый класс исключений - HTTP-ошибок.
    """
    status_code: int = statuses.HTTP_500_INTERNAL_SERVER_ERROR
    body: str = 'A server error occurred.'

    def __init__(self, body: Optional[str] = None):
        self.body = body or self.body

    @property
    def status(self) -> str:
        status_text: str = responses.get(self.status_code, '').title()

        return f"{self.status_code} {status_text}"


class MethodNotAllowed(HTTPException):
    """
    Исключение при попытке получить не существующий модуль
    """
    status_code: int = statuses.HTTP_405_METHOD_NOT_ALLOWED
    body: str = 'Method "{method}" not allowed.'

    def __init__(self, method: str, body: Optional[str] = None):
        self.body = body or self.body.format(method=method)


class BadRequest(HTTPException):
    """
    Исключение при получении не валидных запроса
    """
    status_code: int = statuses.HTTP_400_BAD_REQUEST
    body: str = 'Bad Request'

    def __init__(self, body: Optional[str] = None):
        self.body = body or self.body
