# TODO import module for vk
# TODO import module for telegram


# WSGI main
def application(environ, start_response):
    method = environ.get('REQUEST_METHOD')
    path = environ.get('PATH_INFO')
    if method == 'POST':
        start_response('200 OK', [('Content-Type', 'application/json')])
        if path == '/vk':
            # TODO call vk handler
            pass
        elif path == '/telegram':
            # TODO call telegram handler
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
