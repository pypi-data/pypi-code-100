from pathlib import Path
from typing import Optional

import PIL.IcoImagePlugin
import PIL.PngImagePlugin
from starlette.requests import Request
from starlette.responses import FileResponse, Response
from urlobject.path import URLPath

PURPOSE_VALUE_SET = set(("any", "monochrome", "maskable"))


class Icon:
    def __init__(self, ns: URLPath, path: URLPath, purpose: Optional[str] = None):
        self.ns = ns
        self.path = path
        if purpose and not set(purpose.split()).issubset(PURPOSE_VALUE_SET):
            raise ValueError("invalid purpose value")
        self.purpose = purpose  # TODO: store set?

    @property
    def src(self) -> str:
        return self.ns.add(self.path)

    @property
    def sizes(self) -> str:
        raise NotImplementedError

    @property
    def type(self) -> str:
        raise NotImplementedError

    @property
    def image(self) -> PIL.ImageFile.ImageFile:
        raise NotImplementedError

    def has(self, size: str) -> bool:
        return size in self.sizes.split()

    def to_dict(self) -> dict:
        result = dict(src=self.src, sizes=self.sizes, type=self.type)
        if self.purpose:
            result["purpose"] = self.purpose
        return result

    async def handle_request(self, request: Request) -> Response:
        raise NotImplementedError


class FileIcon(Icon):
    def __init__(
        self,
        ns: URLPath,
        path: URLPath,
        filename: Path,
        *,
        purpose: Optional[str] = None,
    ):
        super().__init__(ns, path, purpose=purpose)
        self.filename = filename

    async def handle_request(self, request: Request) -> Response:
        return FileResponse(self.filename, media_type=self.type)


class PngIcon(FileIcon):
    @property
    def sizes(self) -> str:
        return "{}x{}".format(*self.image.size)

    @property
    def type(self) -> str:
        return "image/png"

    @property
    def image(self) -> PIL.ImageFile.ImageFile:
        with open(self.filename, "rb") as fp:
            return PIL.PngImagePlugin.PngImageFile(fp=fp, filename=self.filename)


class IcoIcon(FileIcon):
    @property
    def sizes(self) -> str:
        return " ".join(
            f"{width}x{height}" for width, height in sorted(self.image.info["sizes"])
        )

    @property
    def type(self) -> str:
        return "image/x-icon"

    @property
    def image(self) -> PIL.ImageFile.ImageFile:
        with open(self.filename, "rb") as fp:
            return PIL.IcoImagePlugin.IcoImageFile(fp=fp, filename=self.filename)
