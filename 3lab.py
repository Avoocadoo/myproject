from paste.httpserver import serve
import os

class WsgiMiddleware(object):
    includes = [
    'app.js',
    'react.js',
    'leaflet.js',
    'D3.js',
    'moment.js',
    'math.js',
    'main.css',
    'bootstrap.css',
    'normalize.css',
    ]

    js = ""
    css = ""

    
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):            
        WsgiMiddleware.sort_includes()
        try:
            response = self.app(environ, start_response).decode() 
            if response.find('<head>') >=0:
                data, headend = response.split('</head>')
                response = data + WsgiMiddleware.css + '</head>' + headend
            if response.find('<body>') >=0:
                data, htmlend = response.split('</body>')
                response = data + WsgiMiddleware.js +'</body>' + htmlend
            yield (response).encode()  
        except FileNotFoundError:
            response_code = '404 Not Found'
            response_type = ('Content-Type', 'text/HTML')
            start_response(response_code, [response_type])
            yield ("404 Not Found").encode()

    def sort_includes():
        for include in WsgiMiddleware.includes:
            if(include.split('.')[1] == 'js'):
                WsgiMiddleware.js += '<script src="/_static/' + include + '"></script>\n'
            else:
                WsgiMiddleware.css += '<link rel="stylesheet" href="/_static/' + include + '"/>\n'

def app(environ, start_response):
    current_directory = os.getcwd()
    path = '\index.html'
    file= open(current_directory+path, 'r')
    response_code = '200 OK'
    response_type = ('Content-Type', 'text/HTML')
    start_response(response_code, [response_type])
    data=file.read()
    return data.encode()

# Оборачиваем WSGI приложение в middleware
app = WsgiMiddleware(app)

# Запускаем сервер
serve(app, host='localhost', port=8080)
