from pathlib import Path

from core.app import Response
from core.exceptions import HTTPException
from server import settings


def get_html(template_name: str) -> str:
    """
    Возращает данные шаблона html старницы
    :param template_name: шаблон html страницы
    :return: данные из шаблона html страницы
    """
    template: Path = settings.TEMPLATE_DIR.joinpath(template_name)
    if not template.exists():
        raise FileNotFoundError(f'File {template_name} not found')

    with template.open(mode='r') as file:
        return file.read()


def render_to_response(template_name: str) -> Response:
    return Response(body=get_html(template_name))


def redirect(location: str, permanent: bool = True):
    """
    Перенаправление на указанный url.
    """
    response = Response(status="301 Moved Permanently" if permanent else "302 Found")
    response.headers["Location"] = location

    return response


def exception_to_response(exception: Exception):
    """

    :param exception:
    :return:
    """
    if not isinstance(exception, HTTPException):
        exception = HTTPException()

    return Response(status=exception.status, body=exception.body)
