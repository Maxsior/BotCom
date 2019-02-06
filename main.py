import json
import logging
from social import vk
from social import telegram
import config
import storage
import messages


# WSGI main
def application(environ, start_response):
    config.configure_logger()
    # TODO логировать подключения
    method = environ.get('REQUEST_METHOD')
    path = environ.get('PATH_INFO')
    if method == 'POST':
        start_response('200 OK', [('Content-Type', 'application/json')])
        size = int(environ.get("CONTENT_LENGTH"))
        body = environ.get("wsgi.input").read(size)
        data = json.loads(body.decode('utf-8'))
        if path == '/vk':
            result = vk.parse(data)
        elif path == '/telegram':
            result = telegram.parse(data)
        else:
            result = 'Неизвестная сеть'
        if type(result) == str:
            yield result.encode('utf-8')
        else:
            messages.parse(result)
        yield b''
    else:
        print(environ.get('QUERY_STRING'))
        if path == '/':
            redirect_headers = [('Location', '/pages/')]
            start_response('301 Moved Permanently', redirect_headers)
            yield b''
        else:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            yield b'Page is not found!'
