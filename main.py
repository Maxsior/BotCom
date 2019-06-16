import json
import logging
import config
import messages
import social


# WSGI main
def application(environ, start_response):
    config.configure_logger()
    method = environ.get('REQUEST_METHOD')
    path = environ.get('PATH_INFO')
    if method == 'POST':
        start_response('200 OK', [('Content-Type', 'application/json')])
        size = int(environ.get("CONTENT_LENGTH"))
        body = environ.get("wsgi.input").read(size)
        data = json.loads(body.decode('utf-8'))

        # get module according path
        end = path.find('/', 1)
        module_name = path[1:end] if end != -1 else path[1:]
        logging.info('запрос бота ' + module_name)

        if module_name in social.modules:
            module = social.modules[module_name]
            result = module.parse(data)
        else:
            logging.warning('неизвестный запрос')
            logging.warning(str(data))
            result = 'Неизвестная сеть'

        if type(result) == str:
            yield result.encode('utf-8')
        else:
            messages.forward(result)
            yield b'ok'
    else:
        if path == '/':
            redirect_headers = [('Location', '/pages/')]
            start_response('301 Moved Permanently', redirect_headers)
            yield b''
        else:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            yield b'Page is not found!'
