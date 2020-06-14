from typing import List

from core.app import Request
from core.exceptions import MethodNotAllowed
from core.shortcuts import exception_to_response, render_to_response


class View:
    """
    Базовый класс представления - обработчика HTTP-запросов.
    """

    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def __init__(self):
        pass

    def __call__(self, request: Request, *args, **kwargs):
        return self.dispatch(request, *args, **kwargs)

    def init_request(self, request: Request, *args, **kwargs):
        pass

    def dispatch(self, request: Request, *args, **kwargs):

        try:
            self.init_request(request, *args, **kwargs)

            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)
        except Exception as exc:
            response = exception_to_response(exc)

        return response

    def _allowed_methods(self) -> List[str]:
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]

    def http_method_not_allowed(self, request: Request, *args, **kwargs):
        raise MethodNotAllowed(method=request.method)


class TemplateView(View):
    """

    """
    template_name: str = None

    def get(self, request, *args, **kwargs):
        return render_to_response(self.template_name)
