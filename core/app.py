import json
import re
import sys
import traceback
from typing import Any
from urllib.parse import parse_qs

from core.router import Router


class Request:
    def __init__(self, environ):
        self.environ = environ
        self.path = environ["PATH_INFO"]
        self.method = environ["REQUEST_METHOD"]
        self.headers = {key: value for key, value in environ.items() if key.startswith("HTTP_")}
        self.params = None
        self.GET = parse_qs(environ["QUERY_STRING"])
        self.POST = {}

        if self.method == "POST":
            try:
                content_length = int(environ.get("CONTENT_LENGTH", 0))
            except:
                content_length = 0

            query_string = environ['wsgi.input'].read(content_length).decode("utf-8")
            self.POST = parse_qs(query_string)


class Response:
    def __init__(self, status="200 OK", body="", content_type="text/html"):
        self.status = status
        self.body = str(body)
        self.headers = {"Content-Type": content_type,
                        "Content-Length": str(len(self.body.encode('utf-8')))

                        }

    @property
    def wsgi_headers(self):
        return [(key, value) for key, value in self.headers.items()]

    @property
    def return_value(self):
        return [self.body.encode('utf-8')]


class JsonResponse(Response):
    def __init__(self, body: Any, status="200 OK"):
        body = json.dumps(body)
        super().__init__(status=status, content_type='application/json', body=body)


class WSGIApplication:
    def __init__(self):
        self.routes = {}

    def __call__(self, environ, start_response):
        response = self.dispatch(Request(environ))
        start_response(response.status, response.wsgi_headers)
        return response.return_value

    @staticmethod
    def not_found():
        return Response(status="404 Not Found",
                        body="Page not found."
                        )

    @staticmethod
    def internal_error():
        return Response(status="500 Internal Server Error",
                        body="An error has occurred."
                        )

    def route(self, route_regex):
        def route_decorator(func):
            self.routes[route_regex] = func

        return route_decorator

    def dispatch(self, request):
        for regex, view_func in self.routes.items():
            match = re.search(regex, request.path)
            if match is not None:
                request.params = match.groupdict()

                try:
                    return view_func(request, **request.params)
                except Exception as exc:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    traceback.print_tb(exc_traceback)
                    return self.internal_error()

        return self.not_found()

    def register_module(self, module: Router):
        if not isinstance(module, Router):
            raise TypeError(f"{module} must be an instance of <core.router.Router> class")

        self.routes.update(module.routes)
