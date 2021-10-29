from waitress import serve
from paste.translogger import TransLogger
from repopip import create_app


if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    format = '%(status)s %(REQUEST_METHOD)s %(REQUEST_URI)s'

    print(f'For local use open http://127.0.0.1:{port}')
    serve(TransLogger(create_app(), setup_console_handler=False, format=format, ), host=host, port=port)

