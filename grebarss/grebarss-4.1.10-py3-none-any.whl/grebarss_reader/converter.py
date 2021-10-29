"""Storage module for Converter class"""

import logging
from pathlib import Path

from jinja2 import Template
from xhtml2pdf import pisa

logger = logging.getLogger('app.converter')


class Converter:
    """
    Class for converting news into HTML or PDF received from cacher (--date) or rss_parser (all other cases)"""

    def __init__(self, source, feed: dict, folder_path: str):
        self.folder_path = folder_path
        self.feed = feed
        self.source = source
        """
        :param source: URL of the RSS source. If not specifying RSS source - None
        :param feed: dict with limited news
        :param folder_path: path to the folder where the converted files will be created
        """

    @staticmethod
    def _get_html_with_temp(**kwargs) -> str:
        """
        Gets html string using a template for further conversion
        :param kwargs: data to install into the template
        :return: html str with data
        """
        current_dir = Path(__file__).parent.resolve()
        path_to_templates = Path(current_dir, "templates")

        template = Template(open(Path(path_to_templates, "html_template.jinja2")).read())
        return template.render(**kwargs)

    def to_html(self):
        """Create file with converted feed to HTML format"""
        file_path = Path(self.folder_path, "news.html")

        try:
            logger.info("Start converting feeds to HTML")
            with open(file_path, 'w', encoding='utf-8') as html_file:
                html_file.write(self._get_html_with_temp(
                    feed=self.feed,
                    url=self.source,
                    fonts_path=str(Path(Path(__file__).parent.resolve(), "fonts")),
                ))
        except Exception as exc:
            logger.exception(exc)
        else:
            logger.info(f"HTML saved in {file_path}")

    def to_pdf(self):
        """Create file with converted feed to PDF format"""
        file_path = Path(self.folder_path, "news.pdf")

        try:
            logger.info("Start converting feeds to PDF")
            with open(file_path, 'w+b') as pdf_file:
                pisa.CreatePDF(self._get_html_with_temp(
                    feed=self.feed,
                    url=self.source,
                    fonts_path=str(Path(Path(__file__).parent.resolve(), "fonts")),
                ), dest=pdf_file)
        except Exception as exc:
            logger.exception(exc)
        else:
            logger.info(f"PDF saved in {file_path}")
