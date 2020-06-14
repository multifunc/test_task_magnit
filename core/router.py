from pathlib import Path
from typing import Dict, Callable


class Router:
    routes: Dict[str, Callable] = None

    def __init__(self, module_file: str):
        self.app_path = Path(module_file).parent
        self.app_name = self.app_path.name
        self.routes = {}

    def route(self, route_regex):
        def route_decorator(view_func):
            self.routes[route_regex] = view_func
            return view_func

        return route_decorator

    def add_route(self, route_regex: str, view: Callable):
        if route_regex in self.routes:
            raise ValueError(f'Route {route_regex} already registered')

        self.routes[route_regex] = view

    @property
    def name(self):
        return self.app_name
