import asyncio
import json
import logging
import socket
import ssl

from asyncio import Event
from collections import deque
from enum import Enum, unique
from io import TextIOBase

import websockets

from websockets.protocol import State


log = logging.getLogger("enderturing")


@unique
class RecognitionResultFormat(Enum):
    """Enum of output transcript formats
    jsonl: Recognition returns a serialized json object per line.
    text: Recognition returns an utterance per line in plain text.
    """

    jsonl = 1
    text = 2


class RecognitionStream(TextIOBase):
    """Stream with recognition results.
    You shouldn't create instances of it manually, they are created by `SpeechRecognizer`

    Examples:
        async with recognizer.recognize_file(src, result_format=RecognitionResultFormat.text) as rec:
            line = await rec.readline()
            while line:
                print(line)
                line = await rec.readline()


    """

    def __init__(
        self,
        *,
        asr_url,
        cmd,
        src_file,
        asr_channels,
        sample_rate,
        extra_ws_params,
        res_format,
        include_partials,
        max_ws_queue
    ):
        self._asr_url = asr_url
        self._src_file = src_file
        self._cmd = cmd
        self._asr_channels = asr_channels
        self._sample_rate = sample_rate
        self._extra_ws_params = extra_ws_params or {}
        self._res_format = res_format
        self._include_partials = include_partials
        self._max_ws_queue = max_ws_queue
        self._tracker = None
        self._websocket = None
        self._finished = False
        self._buffer = deque()

    def readable(self) -> bool:
        """Marks that the stream is readable.

        Returns:
            True
        """
        return True

    def seekable(self) -> bool:
        """Marks that the stream is not seekable.

        Returns:
            False
        """
        return False

    def writable(self) -> bool:
        """Marks that the stream is not writable.

        Returns:
            False
        """
        return False

    async def read(self, size=-1) -> str:
        """Reads an entire transcript.

        Args:
            size: Kept for interface compatibility, not used

        Returns:
            Text with an entire transcript of a file. Can be plain text or jsonl depending on recognition settings
        """
        ready = []
        ready_len = 0
        max_len = size if size and size > 0 else 1e9
        while ready_len < max_len and not self._finished:
            if len(self._buffer) == 0:
                event = Event()
                self._tracker["buffer_waiter"] = event
                await event.wait()
            if len(self._buffer) > 0:
                row = self._buffer.popleft()
                ready_len += len(row) + 1
                ready.append(row)
        return "\n".join(ready)

    async def readline(self, size=-1):
        """Reads a next transcript line.

        Args:
            size: Kept for interface compatibility, not used

        Returns:
            Next transcript line or empty string if EOF.
        """
        if len(self._buffer) == 0 and not self._finished:
            event = Event()
            self._tracker["buffer_waiter"] = event
            await event.wait()
        if self._finished and len(self._buffer) == 0:
            return ""
        return self._buffer.popleft()

    async def _close(self) -> None:
        if self._websocket and self._websocket.state == State.OPEN:
            await self._websocket.close()
        # cancel any pending tasks
        for task in [self._tracker["task_reader"], self._tracker["task_sender"]]:
            if not task.done():
                task.cancel()
            else:
                task.result()

    async def __aexit__(self, exc_type, exc, tb):
        await self._close()

    async def _ws_reader(self, websocket, result_format: RecognitionResultFormat, include_partials: bool, tracker):
        try:
            while True:
                response_json = json.loads(await websocket.recv())
                if "ts" in response_json:
                    tracker["received"] = response_json["ts"]
                    if tracker["waiter"] and tracker["sent"] - tracker["received"] < self._max_ws_queue:
                        event = tracker["waiter"]
                        tracker["waiter"] = None
                        event.set()
                if log.isEnabledFor(logging.DEBUG):
                    log.debug(json.dumps(response_json, ensure_ascii=False))
                if "text" in response_json.keys() and response_json["text"]:
                    if result_format == RecognitionResultFormat.text:
                        self._buffer.append(response_json["text"])
                    elif result_format == RecognitionResultFormat.jsonl:
                        self._buffer.append(json.dumps(response_json, ensure_ascii=False))
                elif include_partials and result_format == RecognitionResultFormat.jsonl:
                    self._buffer.append(json.dumps(response_json, ensure_ascii=False))
                if len(self._buffer) and tracker["buffer_waiter"]:
                    event = tracker["buffer_waiter"]
                    tracker["buffer_waiter"] = None
                    event.set()
        except websockets.ConnectionClosed as e:
            log.info("WS read connection closed for %s: %s", str(self._src_file), str(e))
        except Exception as e:
            log.error("WS read error for %s: %s", str(self._src_file), str(e))
        finally:
            self._finished = True
            if tracker["buffer_waiter"]:
                event = tracker["buffer_waiter"]
                tracker["buffer_waiter"] = None
                event.set()

    async def _file_sender(self, websocket, cmd, num_channels, tracker):
        proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE)
        sample_rate = self._sample_rate
        try:
            while True:
                data = await proc.stdout.read(sample_rate)
                if len(data) == 0:
                    await websocket.send('{"eof" : 1}')
                    break
                await websocket.send(data)
                tracker["sent"] += len(data) / num_channels / sample_rate / 2
                if tracker["sent"] - tracker["received"] >= self._max_ws_queue:
                    event = Event()
                    tracker["waiter"] = event
                    await event.wait()
        except websockets.ConnectionClosed as e:
            log.info("WS write connection closed for %s: %s", str(self._src_file), str(e))
        except Exception as e:
            log.error("WS write error for %s: %s", str(self._src_file), str(e))

    def _get_ssl_ctx(self, asr_url: str):
        if asr_url.startswith("wss"):
            ssl_ctx = ssl.create_default_context()
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = ssl.CERT_NONE
        else:
            ssl_ctx = None
        return ssl_ctx

    async def __aenter__(self):
        log.info("Connecting to: '%s'", self._asr_url)
        try:
            websocket = await websockets.connect(self._asr_url, ssl=self._get_ssl_ctx(self._asr_url))
        except socket.gaierror as e:
            log.error("Error during connection to WS: %s", e)
            log.error("Make sure host accessible and DNS records exists for: '%s'", self._asr_url)
            raise
        await websocket.send(
            json.dumps(
                {"config": {"sample_rate": self._sample_rate, "channels": self._asr_channels, **self._extra_ws_params}}
            )
        )
        self._tracker = {
            "sent": 0,
            "received": 0,
            "waiter": None,
            "buffer_waiter": None,
        }
        self._websocket = websocket
        self._tracker["task_sender"] = asyncio.create_task(
            self._file_sender(websocket, self._cmd, self._asr_channels, self._tracker)
        )
        self._tracker["task_reader"] = asyncio.create_task(
            self._ws_reader(websocket, self._res_format, self._include_partials, self._tracker)
        )
        return self
