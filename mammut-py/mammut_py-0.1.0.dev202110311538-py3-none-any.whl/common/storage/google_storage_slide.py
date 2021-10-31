# coding=utf-8
# coding=utf-8

import logging
from collections import namedtuple
import os
from typing import NamedTuple

import httplib2
from oauth2client.tools import argparser
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import discovery
import mammut
from mammut.common import GOOGLE_API_AUTH_LOCAL_WEBSERVER
from mammut.common import GOOGLE_API_AUTH_LOCAL_CREDENTIAL
from mammut.common.google_api import GoogleAPI
from mammut.common.storage.storage_base import SlidesStorageBase

logger = logging.getLogger()


class SlideElement(NamedTuple):
    slideNumber: int
    elementType: str
    content: str


class GoogleStorageSlide(SlidesStorageBase, GoogleAPI):
    def __init__(self):
        SlidesStorageBase.__init__(self)

    @GoogleAPI.ensure_credentials_and_read_limits
    def get_slide_elements(self, presentation_id):
        def getTextFromShape(shape):
            text = ""
            for i, t in enumerate(shape.get("text").get("textElements")):
                if not t.get("textRun") is None:
                    text = text + t.get("textRun").get("content")
            return text[: len(text) - 1]

        presentation = (
            GoogleStorageSlide.SLIDES_SERVICE.presentations()
            .get(presentationId=presentation_id)
            .execute()
        )
        slides = presentation.get("slides")
        namTupleSlideElements = []
        for i, slide in enumerate(slides):
            for j, element in enumerate(slide.get("pageElements")):
                if not element.get("shape") is None:
                    if not element.get("shape").get("text") is None:
                        text = getTextFromShape(element.get("shape"))
                        namTupleSlideElements.append(
                            (SlideElement(j + 1, "text", text),)
                        )
                else:
                    if not element.get("image") is None:
                        imgUrl = element.get("image").get("sourceUrl")
                        namTupleSlideElements.append(
                            (SlideElement(j + 1, "image", imgUrl),)
                        )
        return namTupleSlideElements
