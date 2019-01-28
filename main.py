import json
from config import keys
from social import vk
# TODO import module for telegram


# WSGI main
def application(environ, start_response):
    method = environ.get('REQUEST_METHOD')
    path = environ.get('PATH_INFO')
    if method == 'POST':
        start_response('200 OK', [('Content-Type', 'application/json')])
        size = int(environ.get("CONTENT_LENGTH"))
        body = environ.get("wsgi.input").read(size)
        data = json.loads(body.decode('utf-8'))
        if path == '/vk':
            vk.parse(data)
        elif path == '/telegram':
            # telegram.parse(data)
            pass
        yield b''
    else:
        print(environ.get('QUERY_STRING'))
        if path == '/':
            redirect_headers = [('Location', '/pages/')]
            start_response('301 Moved Permanently', redirect_headers)
            return [b'']
        else:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [b'Page is not found!']
