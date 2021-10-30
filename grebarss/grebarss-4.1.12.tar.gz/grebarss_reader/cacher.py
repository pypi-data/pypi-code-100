"""Storage module for Cacher class"""

from pathlib import Path

import json
import logging
from datetime import datetime

logger = logging.getLogger('app.cacher')


class Cacher:
    """
    Class for saving and retrieving news from the repository (db.json)
    if the variable source == None it means that we use all the sources available in the storage (db.json)
    """

    def __init__(self, source):
        self.source = source
        current_dir = Path(__file__).parent.resolve()
        file_path = Path(current_dir, 'database/db.json')
        self.cache_file_path = file_path
        """
        :param source: URL of the RSS resource
        """

    def cache(self, feed: dict):
        """
        Saves news from rss_parser to the repository (db.json)
        :param feed: dictionary containing news from rss_parser
        """
        logger.info('Module cacher is starting to save news.')

        with open(self.cache_file_path, "r+", encoding="utf-8") as cache_file:
            json_content: str = cache_file.read()
            json_dicts: list = json.loads(json_content)

            url_list = []
            counter = 0

            for elem in json_dicts:
                url_list.append([key for key in elem.keys()])
                if self.source in elem:
                    for item in feed.get('item'):
                        if item not in json_dicts[counter].get(self.source)[0].get('item'):
                            json_dicts[counter].get(self.source)[0].get('item').append(item)
                counter += 1

            logger.debug(f'URL used list - {url_list}')
            if [self.source] not in url_list:
                json_dicts.append({self.source: [feed]})
            logger.debug(f'News for save - {type(json_dicts)}, {json_dicts}')

        with open(self.cache_file_path, "w", encoding="utf-8") as cache_file:
            json.dump(json_dicts, cache_file, indent=4, ensure_ascii=False)
        logger.info('Module cacher is finishing.')

    def get_cache_data(self, date: int) -> dict:
        """
        Creates dictionary of news from the repository (db.json) published on a specific date.
        :param date: value date in %Y%m%d format
        :return: dict containing news from repository (db.json)
        """
        out_dict_one_source = {'item': []}
        out_dict_all_sources = {'item': []}

        with open(self.cache_file_path, "r", encoding="utf-8") as cache_file:
            json_dicts: list = json.loads(cache_file.read())

            if self.source:
                counter_dict_source_pos = 0
                for elem in json_dicts:
                    if self.source in elem:
                        for item in json_dicts[counter_dict_source_pos].get(self.source)[0].get('item'):
                            if date == Cacher._get_convert_date(item['pubDate']):
                                out_dict_one_source.get('item').append(item)
                    counter_dict_source_pos += 1
                logger.debug(f'Out dict with source news from cache - {out_dict_one_source}')
                logger.info('Module cacher is finishing.')
                return out_dict_one_source
            else:
                counter_dict_all_pos = 0
                for elem in json_dicts:
                    for key_url in elem.keys():
                        for item in elem.get(key_url)[0].get('item'):
                            if date == Cacher._get_convert_date(item['pubDate']):
                                item['source'] = key_url
                                out_dict_all_sources.get('item').append(item)
                    counter_dict_all_pos += 1
                logger.debug(f'Out dict with all news from cache - {out_dict_all_sources}')
                logger.info('Module cacher is finishing.')
                return out_dict_all_sources

    @staticmethod
    def _get_convert_date(date: str) -> int:
        """
        Convert date to %Y%m%d format
        :param date: date in RFC 822 format
        :return: parsed date in %Y%m%d format
        """
        allowed_date_formats = [
            "%a, %d %b %Y %H:%M:%S %z",
            "%a, %d %b %Y %H:%M:%S %Z",
            "%Y-%m-%dT%H:%M:%SZ",
        ]
        temp_date = None

        for date_format in allowed_date_formats:
            try:
                temp_date = datetime.strptime(date, date_format)
            except ValueError:
                pass

        if not temp_date:
            raise ValueError(f'{date} - incorrect data format')
        return int(f"{temp_date.year}{temp_date.month:02d}{temp_date.day:02d}")
