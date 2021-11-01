from alive_progress import alive_bar
from alive_progress.animations import bouncing_spinner_factory
import time

def autobar(msg, style="blocks", timems=180, spinner=None):
    items = range(timems)
    with alive_bar(len(items), title=msg, bar=style, spinner=spinner, stats=False,elapsed=False) as bar:
        for z in items:
            time.sleep(.01)
            bar()

autobar("Hacking all the things  ", style="classic")
autobar("Impressing clients      ", style="classic2")
fsk = bouncing_spinner_factory("🌯", 8 , hide=False, overlay=False)
autobar("Getting FSK             ", spinner=fsk, timems=250)
autobar("Exfiltrating client data", style="filling")
autobar("Installing persistence  ", timems=250, style="checks")
autobar("Cleaning up             ", style="ruler2")
