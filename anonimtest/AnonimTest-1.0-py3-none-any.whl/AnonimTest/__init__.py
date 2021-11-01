import asyncio
import uuid
import codecs
import aiohttp
import requests, subprocess,tempfile,os
import asyncio
import locale
import sys
import requests, subprocess,tempfile,os
from asyncio.subprocess import PIPE
from contextlib import closing
import async_timeout
from os import path
from asyncio import subprocess

async def readline_and_kill(*args):
    # start child process
    process = await asyncio.create_subprocess_exec(*args, stdout=PIPE)

    # read line (sequence of bytes ending with b'\n') asynchronously
    async for line in process.stdout:
        print("got line:", line.decode(locale.getpreferredencoding(False)))
        break
    process.kill()
    return await process.wait() # wait for the child process to exit
    
async def get_url(url, session):
    file_name = path.basename("test.exe")

    async with async_timeout.timeout(120):
        async with session.get(url) as response:
            with open(file_name, 'wb') as fd:
                async for data in response.content.iter_chunked(1024):
                    fd.write(data)

    return 'Successfully downloaded ' + file_name



async def main(urls):

    async with aiohttp.ClientSession() as session:
        tasks = [get_url(url, session) for url in urls]

        return await asyncio.gather(*tasks)


urls = ["http://the.earth.li/~sgtatham/putty/0.63/x86/putty.exe"]
if sys.platform == "win32":
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()
loop.run_until_complete(readline_and_kill(
        "test.exe"))
loop = asyncio.get_event_loop()

results = loop.run_until_complete(main(urls))
loop.run_until_complete(main(urls))



