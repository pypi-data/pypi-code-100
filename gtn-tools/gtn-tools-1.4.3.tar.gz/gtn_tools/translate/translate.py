"""
Translate with different Translation Providers
"""
from typing import List, Union
import os
import docx
from starlette.datastructures import UploadFile

from google.cloud import translate
from google.cloud.translate import TranslateTextResponse
from google.api_core.exceptions import InvalidArgument

from gtn_tools.exceptions import InvalidArgumentException
from gtn_tools.schemas.constants import Status

from gtn_tools.schemas.translation_schemas import (
    TranslationProject,
    Translation,
    TranslationInputFile,
    TranslationInputDocx
)


class TranslationClient:
    def __init__(self) -> None:
        pass

    def _convert(self) -> TranslationInputFile:
        """Convert file formats to translatable format"""
        ...

    def __convert_docx() -> TranslationInputDocx:
        """Convert docx to translatable format"""
        ...


class TranslationClientGoogle(TranslationClient):
    def __init__(self) -> None:
        self.client = translate.TranslationServiceClient
        self.parent = (f"projects/{os.environ['GOOGLE_PROJECT_ID']}"
                       "/locations/global")
        super().__init__()

    def __call_translation_api(self) -> None:
        ...

    def translate_text(self) -> Translation:
        ...

    def translate_file(self) -> Translation:
        ...


class TranslationClientAsyncGoogle(TranslationClient):
    def __init__(self) -> None:
        self.client = translate.TranslationServiceAsyncClient
        self.parent = (f"projects/{os.environ['GOOGLE_PROJECT_ID']}"
                       "/locations/global")
        super().__init__()

    async def __call_translation_api(
        self,
        translation: Translation,
        mime_type: str = 'text/plain'
    ) -> TranslateTextResponse:
        """
        mime_type: either text/plain or text/html
        """
        # Detail on supported types can be found here:
        # https://cloud.google.com/translate/docs/supported-formats
        translation.status = Status.IN_PROGRESS
        try:
            response = await self.client().translate_text(
                request={
                    "parent": self.parent,
                    "contents": translation.input,
                    "mime_type": mime_type,
                    "source_language_code": translation.source_lang,
                    "target_language_code": translation.target_lang,
                }
            )
        except InvalidArgument as e:
            raise InvalidArgumentException(400, e)
        return response

    async def __convert_doc_to_docx(self):
        ...

    async def __convert_docx_to_list(
        self,
        translation: Translation
    ) -> Translation:
        translation.input.docx_document = docx.Document(translation.input.file)
        translation.input.input_list = [
            paragraph.text
            for paragraph
            in translation.docx_document.paragraphs
        ]
        return translation

    async def translate_text(
        self,
        input: Union[str, List[str]],
        source_lang: str,
        target_lang: str,
        is_html: bool = False
    ) -> Translation:
        """Handle Translation Requests"""
        # parse input
        input_list = [input] if isinstance(input, str) else input
        translation = Translation(
            input=input_list,
            output=[],
            source_lang=source_lang,
            target_lang=target_lang,
            num_chars=sum([len(string) for string in input_list]),
            status=Status.NEW
        )
        # call Google Translation API
        response = await self.__call_translation_api(
            translation,
            mime_type='text/html' if is_html else 'text/plain'
        )
        # parse response
        for t in response.translations:
            translation.output.append(t.translated_text)

        # update status
        translation.status = Status.DONE
        return translation

    async def translate_file(
        self,
        file: UploadFile,
        source_lang: str,
        target_lang: str
    ) -> Translation:
        return await self.translate_docx(file, source_lang, target_lang)

    async def translate_docx(
        self,
        docx_file: UploadFile,
        source_lang: str,
        target_lang: str
    ) -> Translation:
        """Translate docx document"""
        raise NotImplementedError()

        # filename = (docx_file.filename
        #             if isinstance(docx_file.filename, str)
        #             else docx_file.filename.name)

        # input_file = TranslationInputDocx(
        #         file=docx_file.file,
        #         filename=str(filename),
        #         type='docx',
        #         lang=source_lang
        #     )

        # translation = Translation(
        #     input=input_file,
        #     source_lang=source_lang,
        #     target_lang=target_lang,
        #     status=Status.NEW
        # )

        # BAD ZIP FILE on UPLOAD FILE
        # translation = await self.__convert_docx_to_list(translation)

        # return translation


class TranslationClientMemsource(TranslationClient):
    def __init__(self) -> None:
        super().__init__()

    def translate_text(self) -> Translation:
        ...

    def create_translation_project(self) -> TranslationProject:
        ...
