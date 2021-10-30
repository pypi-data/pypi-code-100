"""Storage module for classes RssParser"""

import os
import sys
import json

import logging
import re

import xmltodict

sys.path.append(os.path.dirname(os.getcwd()))

import grebarss_reader.urlmarker as urlmarker
import grebarss_reader.config as config
from grebarss_reader.cacher import Cacher
from grebarss_reader.converter import Converter
from grebarss_reader.getter import GetterXml
from grebarss_reader.printer import Printer

logger = logging.getLogger('app.rss_parser')


class RssParser:
    """Class for parsing response received by getter.py and printing result"""

    @staticmethod
    def _get_image_link(item: dict) -> str:
        url_list = set(re.findall(urlmarker.URL_REGEX, str(item)))
        logger.debug(f'{type(url_list)}Url list - {url_list}')
        for link in url_list:
            if link.endswith('.jpg') or link.endswith('.jpeg') or link.endswith('.png') or link.startswith(
                    'https://s.yimg') or link.startswith('https://i.guim'):
                return link

    @staticmethod
    def _get_raw_feed(source: str):
        """
        Transform XML data to dict with all news
        :arg source: URL source with news
        :return: dictionary with raw feed (all news)
        """
        raw_feed = xmltodict.parse(GetterXml().get_response(source).text, encoding='utf-8')
        logger.debug(f'All news in raw dict (feed) - {raw_feed}')
        return raw_feed

    @staticmethod
    def _parse_xml(raw_feed) -> dict:
        """
        Transform XML data to dict
        :arg args: set of arguments
        :return: dictionary with XLM data
        """
        data_dict_out = {"item": []}

        for item in raw_feed['rss']['channel']['item']:
            data_dict_out['item'].append(
                {"title": item.get("title"),
                 "pubDate": item.get("pubDate"),
                 "link": item.get("link"),
                 "image": RssParser._get_image_link(item)})

        logger.debug(f'All news in final dict - {data_dict_out}')
        return data_dict_out

    @staticmethod
    def _limit(data: dict, limit: int) -> dict:
        out_dict = dict()
        out_dict['item'] = (data['item'][:limit])
        return out_dict

    @staticmethod
    def start():
        """ Start work with rss_parser"""
        logger.info("Module rss_parser is starting.")

        args = config.AppArgParser().get_args()
        logger.debug(f'Argparse sent these arguments - {args.__dict__}')

        if args.verbose:
            config.AppLogger.activate_verbose()
            logger.info(f'Verbose mode activated.')

        parser = RssParser()

        if args.date:
            cache: dict = Cacher(args.source).get_cache_data(args.date)
            limited_cache = RssParser._limit(cache, args.limit)
            logger.debug(f'limited cache - {limited_cache}')
            if args.to_html:
                Converter(args.source, limited_cache, args.to_html).to_html()
            elif args.to_pdf:
                Converter(args.source, limited_cache, args.to_pdf).to_pdf()
            else:
                Printer().print_info(limited_cache)
        else:
            feed: dict = parser._parse_xml(parser._get_raw_feed(args.source))
            limited_feed = RssParser._limit(feed, args.limit)
            logger.debug(f'limited feed for cache - {limited_feed}')
            Cacher(args.source).cache(limited_feed)

            if args.json:
                logger.info(f'Json mode activated.')
                Printer().print_info_json(limited_feed)
                if args.to_html:
                    Converter(args.source, limited_feed, args.to_html).to_html()
                elif args.to_pdf:
                    Converter(args.source, limited_feed, args.to_pdf).to_pdf()
            else:
                if args.to_html:
                    Converter(args.source, limited_feed, args.to_html).to_html()
                elif args.to_pdf:
                    Converter(args.source, limited_feed, args.to_pdf).to_pdf()
                else:
                    Printer().print_info(limited_feed)
