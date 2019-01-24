from wsgiref.simple_server import make_server
from main import application

PORT = 8080
with make_server('', PORT, application) as httpd:
    print("Serving HTTP on port {}...".format(PORT))
    httpd.serve_forever()
