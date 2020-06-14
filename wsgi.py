from wsgiref.simple_server import make_server

from core.app import WSGIApplication
from server.wsgi import get_wsgi_application

app: WSGIApplication = get_wsgi_application()

HOST: str = "0.0.0.0"
PORT: int = 8000

if __name__ == '__main__':
    http = make_server(HOST, PORT, app)

    print(f"Serving on http://{HOST}:{PORT}")
    http.serve_forever()
