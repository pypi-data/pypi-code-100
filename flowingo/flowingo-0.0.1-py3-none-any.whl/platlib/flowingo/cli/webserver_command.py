import click
import uvicorn

from flowingo.configuration import conf


@click.command()
@click.option('-p', '--port', type=int, default=8080, show_default=True, help='Webserver port')
@click.option('--debug', is_flag=True, default=False, show_default=True, help='Debug webserver')
@click.option('-d', '--demonize', is_flag=True, default=False, show_default=True, help='Demonize webserver')
def webserver(port: int, debug: bool, demonize: bool):
    """Starts flowingo webserver"""
    print('webserver !!')
    conf.webserver_debug = debug
    conf.webserver_port = port
    conf.webserver_demonize = demonize

    uvicorn.run(
        "app.app:app",
        host='0.0.0.0',
        port=port,
        reload=True,
        debug=True,
        workers=1
    )
