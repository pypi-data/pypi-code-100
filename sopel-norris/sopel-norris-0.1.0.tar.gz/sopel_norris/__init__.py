# coding=utf8
"""sopel-norris

Chuck Norris joke plugin for Sopel IRC bots.
"""
from __future__ import unicode_literals, absolute_import, division, print_function

import random

import requests

from sopel import formatting, module
from sopel.tools import SopelMemory, get_logger, web


LOGGER = get_logger('norris')


class APIError(Exception):
    """Just a custom exception type to throw from API helpers."""
    pass


class InvalidQueryError(Exception):
    """The API likes to throw 400 Bad Request instead of returning JSON with an error message."""
    pass


class NoResultError(Exception):
    """Tin."""
    pass


def setup(bot):
    bot.memory['norris_cache'] = SopelMemory()


def shutdown(bot):
    try:
        del bot.memory['norris_cache']
    except KeyError:
        pass


@module.commands('norris', 'chucknorris')
@module.output_prefix('[CNJ] ')
def chuck_norris(bot, trigger):
    """Fetch a random Chuck Norris joke, with optional keyword search."""
    arg = trigger.group(2)
    if arg is not None and arg.strip():
        try:
            joke = fetch_results(bot, arg)
        except APIError:
            bot.reply(
                "Something went wrong. Try again later! "
                "(If this keeps happening, ask %s to check my error logs.)"
                % bot.config.core.owner
            )
            return
        except InvalidQueryError:
            bot.reply(
                "The query couldn't be processed. Make sure it's just a keyword "
                "or three, no punctuation."
            )
            return
        except NoResultError:
            bot.reply("No matching jokes.")
            return
    else:
        try:
            joke = fetch_random()
        except APIError:
            bot.reply(
                "Something went wrong. Try again later! "
                "(If this keeps happening, ask %s to check my error logs.)"
                % bot.config.core.owner)
            return

    bot.say(joke)


API_BASE = 'https://api.chucknorris.io/'
JOKES = API_BASE + 'jokes'
RANDOM = JOKES + '/random'
SEARCH = JOKES + '/search?query=%s'


def fetch_random():
    try:
        r = requests.get(RANDOM)
        data = r.json()
        joke = data['value']
    except Exception as err:
        # I'm tired of writing half a dozen cases all the time. Just log it.
        LOGGER.error("Couldn't fetch random Chuck Norris joke: %s", err)
        raise APIError

    return joke


def fetch_results(bot, query):
    query = formatting.plain(query.strip())
    cache = bot.memory['norris_cache'].get(query, [])

    if cache:
        return cache.pop()

    try:
        r = requests.get(SEARCH % web.quote(query))
        data = r.json()
    except Exception as err:
        # No case-by-case handling here. Just log it and give up.
        LOGGER.error("Couldn't search Chuck Norris jokes: %s", err)
        raise APIError

    if r.status_code == 400:
        raise InvalidQueryError

    jokes = [item['value'] for item in data['result']]
    random.shuffle(jokes)

    if not jokes:
        raise NoResultError

    # the list of matching jokes might be quite large; take one
    # and store the rest for later calls on the same query
    # since the chucknorris.io API doesn't support pages/limits
    bot.memory['norris_cache'][query] = jokes[1:]
    return jokes[0]
