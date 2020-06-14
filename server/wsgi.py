from core.app import WSGIApplication

from server.apps.comments.urls import router as comments_routes
from server.db import _init_db


def get_wsgi_application() -> WSGIApplication:
    """
    Возвращает экземпляр WSGI-приложения.
    """
    app = WSGIApplication()

    app.register_module(comments_routes)

    _init_db()

    return app
