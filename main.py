from config import keys

# TODO import module for vk

# TODO import module for telegram

# WSGI main
def application(environ, start_response):
    method = environ.get('REQUEST_METHOD')
    path = environ.get('PATH_INFO')
    if method == 'POST':
        start_response('200 OK', [('Content-Type', 'application/json')])
        if path == '/vk':
            # vk.send_message(msg = text, to = username, auth = keys['vk'])
            pass
        elif path == '/telegram':
            # telegram.send_message(msg = text, to = username, auth = keys['tg'])
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
