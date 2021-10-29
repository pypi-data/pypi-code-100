import json
import logging
from functools import wraps
from time import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd

from .exceptions import VkApiError, VkHttpError, VkError
from .util.parsers import parse_friends_df
from .config import Default


class VkApiSess(object):
    """
    Custom vk api class for comfortable usage/expansion

    NB!: Для большей гибкости кода, экземпляр Сессии можно явно передать,
    если нет - генерируется новый и сразу задается:
    Retry стратегия c backoff_factor (на ошибки 5**),
    дефолтный timeout.

    Args:
        access_token: User access token (README has instructions on how to get one)
        api_version: VK API version used for making requests
        app_id: authorized app id used for requests
        base_url: vk api base url
        session: session object, created if not given. Defaults to None.
        sets retry strategy and backoff factor for server-end erorrs.
        sess_retries: Number of max retries.
        sess_backoff: Backoff coefficient.
        sess_timeout: request timeout. (so app wont block)
    """
    def __init__(self,
                 access_token: str,
                 api_version: str,
                 app_id: int,
                 base_url: str,
                 session=None,
                 sess_retries: int = Default.RETRIES,
                 sess_backoff: int = Default.BACKOFF,
                 sess_timeout: int = Default.TIMEOUT):

        # configure session
        self.http = session or requests.Session()
        retries = Retry(
            total=sess_retries, backoff_factor=sess_backoff,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.http.mount('http://', adapter)
        self.http.mount('https://', adapter)

        self.api_version = api_version
        self.app_id=app_id
        self.base_url = base_url
        self.api_version = api_version
        self.token = access_token
        self.temp_df = []
        self.timeout = sess_timeout

        logging.info("VkAPI session created")
        logging.info(f"Current app id: {self.app_id}")
        logging.info(f"Using api ver: {self.api_version}")
        logging.info(f"API base url: {self.base_url}")

    @staticmethod
    def timing(f):
        @wraps(f)
        def wrap(*args, **kw):
            t_start = time()
            result = f(*args, **kw)
            t_end = time()
            print('func:%r args:[%r, %r] took: %2.4f sec' % \
            (f.__name__, args, kw, t_end-t_start))
            return result
        return wrap

    def token_validation(self) -> bool:
        """Validate token/successful connection to api.

        Returns:
            bool: True if token is valid, else False
        """
        try:
            self.method_execute(
                method='stats.trackVisitor'
            )
        except VkApiError:
            return False
        return True

    def method_execute(self,
                       method: str,
                       values: dict = None,
                       response_raw: bool = False):
        """Execute any api method with any values (if given method supports them).
        Also catches most common errors.

        NB!: Обработка исключений для requests и внутри самого API:
        raise_for_status ловит HTTTPError;
        Ошибки 5** повторно отправляют запросы (session.Retry стратегия).
        
        Для удобства пользователя (чтобы не пугать кучей непонятных символов),
        большинство исключений вызывают sys.exit и краткое описание ошибки.
        Подробная информация записывается в файл с логами.

        Ошибки внутри самого API возвращают status_code=200 и полноценный json.response,
        Поэтому каждый ответ проверяем на наличие ключа 'error'.
        Если ошибка - пытаемся донести причину и выходим.

        Args:
            method: VkAPI method (e.g.users.get, friends.)
            values: Dict of params for request url. Defaults to None.
            response_raw: 
                        if False - rerutns response['response'],
                        if True - returns response. Defaults to False.
        Raises:
            VkHttpError: Handle HTTP Errors
            VKApiError: Handle API Errors
            VkError: Base exceptions handler
            SystemExit: exit interpreter with code: [
                4 - HTTP,
                5 - ConnectionError,
                6 - Timeout,
                10 - Unknown Error] 
        Returns:
            requests.response or requests.response['response']
        """

        values = values.copy() if values else {}
        if 'v' not in values:
            values['v'] = self.api_version
        if self.token:
            values['access_token'] = self.token

        # query = f"{self.base_url}/{method}?access_token={self.token}&v={self.api_version}"
        try:
            response = self.http.get(
                self.base_url + method,
                params=values,
                timeout=self.timeout
            )
            response.raise_for_status()

        except requests.exceptions.HTTPError as errh:
            logging.debug(f"HTTP Error: {str(errh)}")
            print(errh)
            raise SystemExit(4)

        except requests.ConnectionError as errc:
            logging.debug(f"Error Connecting: {str(errc)}")
            print(f"{type(errc).__name__} (see full error in logs). Failed to establish connection. Exiting..")
            raise SystemExit(5)

        except requests.exceptions.Timeout as errt:
            logging.debug(f"Timeout Error: {str(errt)}")
            print(f"{type(errt).__name__} (see full error in logs). Server didnt response in time. Exiting..")
            raise SystemExit(6)

        except requests.exceptions.RequestException as err:
            logging.debug(f"Unexpected Error: {str(err)}")
            print(f"Unexpected Error Occured: {type(err).__name__}. (see full error in logs)")
            raise SystemExit(10)

        response = response.json()

        if 'error' in response:
            raise VkApiError(response['error']) from None

        return response if response_raw else response['response']

    def get_friends(self,
                    fields: list,
                    search_user_id: int,
                    offset: int = 0,
                    mpr_count: int = 2000,
                    fids_count: int = None):
        """Get user's friends and transform into pandas dataframe,
        which contains ONLY the specified fields (bdate, city etc.).

        NB!: Максимальное кол-во друзей вк - 10к. Кап на один запрос - 5к =>
        необходима пагинация. Чтобы не хранить по 5к объектов в одной переменной
        установим кап 1000 и будем порционно выгружать, перезаписывая переменную.

        Для удобного анализа, обработки, экспорта и тд. решил использовать pandas.
        Для сохранения промежуточного состояния использую self.temp_df,
        из которого потом собираю dataframe. Такой вариант оптимальнее, чем
        наращивать dataframe в цикле через pd.df.append() или pd.df.concat() тк
        эти методы каждый раз возвращают новый объект-копию => O(N^2), такой себе вариант.

        Args:
            fields: List of values to return for each friend
            search_user_id: ID of a user, whose friendlist to return
            offset: Entry point for request. Defaults to 0.
            mpr_count: Max users per request. Defaults to 100.
            order: order in which to return friendlist. Defaults to 'name'.

        Returns:
            pandas DataFrame, reshaped accordingly to the parser function
        """
        values={
            "user_id": search_user_id,
            "count": mpr_count,
            "offset": offset,
            "fields": fields
            }

        logging.info(f"Getting friends of user:{search_user_id}")
        logging.info(f"Aditional fields to get: {fields}")
        # logging.info(f"Specified order: {order}")

        response = self.method_execute(
            method='friends.get', values=values
        )
        count = fids_count or response['count']
        self.temp_df += response['items']
        logging.info(f"{len(self.temp_df)} of {count} friends parsed")

        offset += mpr_count
        if int(count) > mpr_count and offset < int(count):
            logging.debug(f"current offset: {offset}; count: {count}. Repeat request")

            return self.get_friends(
                search_user_id=search_user_id,
                offset=offset, fields=fields,
                fids_count=fids_count
            )

        logging.info(f"All friends collected. Amount: {len(self.temp_df)}")    
        logging.debug("Building dataframe from summed json response")
        
        friends_df = pd.json_normalize(self.temp_df)

        return parse_friends_df(friends_df)
