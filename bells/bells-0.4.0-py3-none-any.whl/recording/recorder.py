"Recorder used in bells"

import asyncio
import logging

import questionary as qu
import sounddevice as sd
import soundfile as sf

from .. import colors


def samplerate():
    "Gets sample rate for default input device"
    device_info = sd.query_devices(None, 'input')
    logging.info("device_info %s", device_info)
    return int(device_info['default_samplerate'])


async def _prompt(pause, stop, style):
    "Asks for user input"
    recording = qu.select("Recording", ["stop", "pause"], style=style)
    paused = qu.select("Paused", ["stop", "resume"], style=style)

    while True:
        if pause.is_set():
            res = await paused.ask_async()
        else:
            res = await recording.ask_async()
        if res == "pause":
            pause.set()
        elif res == "resume":
            pause.clear()
        elif res == "stop":
            stop.set()
            break


async def _recorder(pause, stop, file):
    "Records audio"
    def callback(indata, *_):
        if pause.is_set():
            return
        file.write(indata.copy())

    stream = sd.InputStream(samplerate=samplerate(), channels=1,
                            callback=callback)
    with stream:
        await stop.wait()


async def interactive_recorder_async(path, style):
    "Simple interactive recorder"
    pause = asyncio.Event()
    stop = asyncio.Event()
    with sf.SoundFile(path, 'w', samplerate=samplerate(), channels=1) as file:
        await asyncio.gather(_recorder(pause, stop, file),
                             _prompt(pause, stop, style))


def interactive_recorder(path, *, style=colors.style):
    "Wraps the async variant to create a sync variant"
    asyncio.run(interactive_recorder_async(path, style))
