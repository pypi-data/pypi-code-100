"""Handle the startup/shutdown process."""
import tornado

from asyncio import sleep

from .handlers import send_message, completed, messageReceivedEvent
from .distributor import distribute, precalculate
from .scripts import run_startup_scripts, run_shutdown_scripts
from .services import start_services, shutdown_services


async def startup(settings):
    """Run the startup process.

    :param settings: The settings to use for startup
    :type settings: dict
    """
    send_message({'message': 'Container starting up...'})
    await distribute(settings)
    await run_startup_scripts(settings)
    await start_services(settings)
    completed()
    await sleep(0.001)
    await messageReceivedEvent.wait()
    tornado.ioloop.IOLoop.current().stop()


async def shutdown(settings):
    """Run the shutdown process.

    :param settings: The settings to use for shutdown
    :type settings: dict
    """
    await shutdown_services(settings)
    await run_shutdown_scripts(settings)
    await sleep(0.001)
    tornado.ioloop.IOLoop.current().stop()


async def prepare(settings):
    """Run the content preparation process.

    :param settings: The settings to use for shutdown
    :type settings: dict
    """
    await precalculate(settings)
    await sleep(0.001)
    tornado.ioloop.IOLoop.current().stop()


async def only_distribute_files(settings):
    """Run only the content distribution process and exist.

    :param settings: The settings to use for distributing files
    :type settings: dict
    """
    await distribute(settings)
    tornado.ioloop.IOLoop.current().stop()
