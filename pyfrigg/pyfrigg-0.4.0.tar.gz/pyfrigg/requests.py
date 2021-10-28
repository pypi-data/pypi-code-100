from typing import Dict, Tuple, List, Union
from tqdm.asyncio import tqdm
from functools import reduce
import logging
import asyncio
import aiohttp

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())
LOGGER.setLevel("WARNING")


def _squeeze(input: List[dict], mapping: Dict[str, Tuple[str]]) -> List[dict]:
    """
    Squeeze list of dicts

    :param input: list of nested dicts
    :param mapping: dict mapping field names to their paths in nested dicts
    """

    def get_nested(dict_: dict, path: Tuple[str]) -> Union[str, None]:
        try:
            return reduce(lambda x, y: x.get(y, None), path, dict_)
        except Exception:
            return None

    return [{y: get_nested(x, mapping[y]) for y in mapping.keys()} for x in input]


async def _get_response_body(
    url: str,
    session: aiohttp.ClientSession,
    request: str = "get",
    dict_: bool = False,
    **kwargs,
) -> Union[dict, str]:
    """
    Return response body as str or dict asynchronously

    :param url: url to request
    :param session: current aiohttp.ClientSession instance
    :param request: one of get, put, post, and delete
    :param dict_: if True return response body as json, otherwise return response body as str
    """
    try:
        async with getattr(session, request)(url=url, **kwargs) as response:
            if dict_:
                return await response.json()
            else:
                return await response.text()

    except Exception as exception:
        LOGGER.info(f"Unable to get url {url} due to\n{exception}.")


async def _gather_response_bodies(
    urls: List[str],
    request: str = "get",
    dict_: bool = False,
    verbose: int = 0,
    **kwargs,
) -> List[Union[str, dict]]:
    """
    Return list of response bodies as str or dict asynchronously

    :param urls: list of urls to request
    :param request: one of get, put, post, and delete
    :param dict_: if True return response body as json, otherwise return response body as str
    :param verbose: if > 0, show tqdm progress bar
    """
    async with aiohttp.ClientSession() as session:
        responses = [
            _get_response_body(
                url=urls[i],
                session=session,
                request=request,
                dict_=dict_,
                **{key: value[i] for key, value in kwargs.items()},
            )
            for i in range(len(urls))
        ]
        responses = tqdm.gather(
            *responses,
            bar_format="{l_bar}{bar:50}{r_bar}{bar:-10b}",
            colour="blue",
            disable=verbose == 0,
        )
        return await responses


def _request(
    urls: List[str],
    request: str = "get",
    mapping: Union[Dict[str, Tuple[str]], None] = None,
    verbose: int = 0,
    **kwargs,
) -> List[Union[dict, str]]:
    """
    Return list of squeezed response bodies as dict if mapping, otherwise return list of response bodies as str
    Basic request method

    :param request: one of get, put, post, post, and delete
    :param urls: list of urls to request
    :param mapping: dict of field names and field paths to extract from request body as json
    :param verbose: if > 0, show tqdm progress bar
    """
    if mapping is None:
        return asyncio.run(
            _gather_response_bodies(
                urls=urls,
                request=request,
                dict_=False,
                verbose=verbose,
                **kwargs,
            ),
        )
    else:
        return _squeeze(
            asyncio.run(
                _gather_response_bodies(
                    urls=urls,
                    request=request,
                    dict_=True,
                    verbose=verbose,
                    **kwargs,
                )
            ),
            mapping=mapping,
        )


def get(
    urls: List[str],
    mapping: Union[Dict[str, Tuple[str]], None] = None,
    verbose: int = 0,
    **kwargs,
) -> List[Union[dict, str]]:
    """
    Return list of squeezed response bodies as dict if mapping, otherwise return list of response bodies as str

    :param request: one of get, put, post, post, and delete
    :param urls: list of urls to request
    :param mapping: dict of field names and field paths to extract from request body as json
    """
    return _request(
        request="get",
        urls=urls,
        mapping=mapping,
        verbose=verbose,
        **kwargs,
    )


def post(
    urls: List[str],
    mapping: Union[Dict[str, Tuple[str]], None] = None,
    verbose: int = 0,
    **kwargs,
) -> List[Union[dict, str]]:
    """
    Return list of squeezed response bodies as dict if mapping, otherwise return list of response bodies as str

    :param request: one of get, put, post, post, and delete
    :param urls: list of urls to request
    :param mapping: dict of field names and field paths to extract from request body as json
    """
    return _request(
        request="post",
        urls=urls,
        mapping=mapping,
        verbose=verbose,
        **kwargs,
    )


def put(
    urls: List[str],
    mapping: Union[Dict[str, Tuple[str]], None] = None,
    verbose: int = 0,
    **kwargs,
) -> List[Union[dict, str]]:
    """
    Return list of squeezed response bodies as dict if mapping, otherwise return list of response bodies as str

    :param request: one of get, put, post, post, and delete
    :param urls: list of urls to request
    :param mapping: dict of field names and field paths to extract from request body as json
    """
    return _request(
        request="put",
        urls=urls,
        mapping=mapping,
        verbose=verbose,
        **kwargs,
    )


def delete(
    urls: List[str],
    mapping: Union[Dict[str, Tuple[str]], None] = None,
    verbose: int = 0,
    **kwargs,
) -> List[Union[dict, str]]:
    """
    Return list of squeezed response bodies as dict if mapping, otherwise return list of response bodies as str

    :param request: one of get, put, post, post, and delete
    :param urls: list of urls to request
    :param mapping: dict of field names and field paths to extract from request body as json
    """
    return _request(
        request="delete",
        urls=urls,
        mapping=mapping,
        verbose=verbose,
        **kwargs,
    )
