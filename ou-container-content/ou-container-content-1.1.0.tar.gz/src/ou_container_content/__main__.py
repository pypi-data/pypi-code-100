"""The OU Container Content distribution application commandline interface."""
import click
import os
import tornado.ioloop
import tornado.web

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from .handlers import WebsocketHandler, StaticHandler, console_handler
from . import process
from .validator import validate_settings


def make_app():
    """Build the tornado web application."""
    return tornado.web.Application([
        (r".*websocket", WebsocketHandler),
        (r".*build/(.*)", StaticHandler, {'base_path': 'build/'}),
        (r".*(global.css)", StaticHandler, {'base_path': ''}),
        (r".*(ou-favicon-[0-9]+.png)", StaticHandler, {'base_path': ''}),
        (r".*", StaticHandler, {'base_path': 'index.html'}),
    ])


@click.group()
@click.option('-c', '--config',
              type=click.File(),
              default='/etc/module-content/config.yaml',
              help='The configuration file to use')
@click.pass_context
def main(ctx: click.Context, config: click.File):
    """OU Container Content distribution."""
    settings = load(config, Loader=Loader)
    settings = validate_settings(settings)
    if isinstance(settings, dict):
        ctx.obj = {'settings': settings}
    else:
        click.echo(click.style('There are errors in your configuration settings:', fg='red'), err=True)
        click.echo(err=True)

        for error in settings:
            click.echo(error, err=True)

        raise click.Abort()


@click.command()
@click.pass_context
def startup(ctx: click.Context):
    """Run the startup process."""
    app = make_app()
    app.listen(8888)
    if 'JUPYTERHUB_API_TOKEN' not in os.environ:
        tornado.ioloop.IOLoop.current().add_callback(console_handler)
    tornado.ioloop.IOLoop.current().add_callback(process.startup, ctx.obj['settings'])
    tornado.ioloop.IOLoop.current().start()


@click.command()
@click.pass_context
def shutdown(ctx: click.Context):
    """Run the shutdown process."""
    tornado.ioloop.IOLoop.current().add_callback(process.shutdown, ctx.obj['settings'])
    tornado.ioloop.IOLoop.current().start()


@click.command()
@click.pass_context
def prepare(ctx: click.Context):
    """Run the distribution preparation process."""
    tornado.ioloop.IOLoop.current().add_callback(process.prepare, ctx.obj['settings'])
    tornado.ioloop.IOLoop.current().start()


@click.command()
@click.pass_context
def distribute_content(ctx: click.Context):
    """Run the content distribution only."""
    tornado.ioloop.IOLoop.current().add_callback(process.only_distribute_files, ctx.obj['settings'])
    tornado.ioloop.IOLoop.current().start()


main.add_command(startup)
main.add_command(shutdown)
main.add_command(prepare)
main.add_command(distribute_content)

if __name__ == '__main__':
    main()
