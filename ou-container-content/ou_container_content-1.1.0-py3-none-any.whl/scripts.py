"""Run scripts."""
import math

from asyncio.subprocess import create_subprocess_exec

from .handlers import send_message


async def run_startup_scripts(settings):
    """Run all startup scripts.

    :param config: The configuration with the scripts to run
    :type config: dict
    """
    send_message({
        'message': 'Running startup scripts...'
    })
    send_message({
        'component': 'scripts',
        'state': 'active',
        'progress': 0,
    })
    if 'scripts' in settings and 'startup' in settings['scripts']:
        for idx, script in enumerate(settings['scripts']['startup']):
            if 'cmd' in script:
                proc = await create_subprocess_exec(*script['cmd'].split(' '))
                await proc.wait()
            send_message({
                'component': 'scripts',
                'state': 'active',
                'progress': math.floor(100 / len(settings['scripts']) * idx),
            })
    send_message({
        'component': 'scripts',
        'state': 'complete',
        'progress': 100,
    })


async def run_shutdown_scripts(settings):
    """Run all shutdown scripts.

    :param config: The configuration with the scripts to run
    :type config: dict
    """
    if 'scripts' in settings and 'shutdown' in settings['scripts']:
        for script in settings['scripts']['shutdown']:
            if 'cmd' in script:
                proc = await create_subprocess_exec(*script['cmd'].split(' '))
                await proc.wait()
