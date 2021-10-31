from yarl import URL
from aiohttp import (
    ClientSession,
    ClientResponse,
    ClientResponseError,
    ClientConnectionError,
)
from json.decoder import JSONDecodeError
from . import API_KEY

from .exceptions import APIError, JsonFormatError, NotFoundError
from .urls import Urls

DATA = "data"


class MiningPoolHubAPI(object):
    def __init__(self, session: ClientSession, api_key: str = API_KEY):
        self.__client = session
        self.__api_key = {"api_key": api_key}
        self.urls = Urls()

    def api_key_set(self):
        return self.__api_key is not None

    @staticmethod
    async def __to_json(response: ClientResponse):
        """Private method to call json method on response object

        Parameters
        ----------
        response : ClientResponse
            The response object

        Returns
        -------
        dict
            JSON response represented as a Python dictionary
        """
        return await response.json(content_type="text/html")

    async def __get_data(self, url: URL):
        """Private method to make a GET request to the URL

        Parameters
        ----------
        url : str
            The URL to query

        Returns
        -------
        dict
            JSON response represented as a Python dictionary

        Raises
        ------
        HTTPError
            Raises on HTTP Error
        JSONDecodeError
            Raises when there is an issue parsing the JSON response
        """
        try:
            response = await self.__client.get(url % self.__api_key)

            # raises if the status code is an error - 4xx, 5xx
            response.raise_for_status()

            return await self.__to_json(response)
        except ClientResponseError as e:
            raise APIError(e)
        except ClientConnectionError as e:
            raise NotFoundError(e)
        except JSONDecodeError as e:
            raise JsonFormatError(e)

    async def async_get_block_count(self, coin_name: str):
        """ "Get current block height in blockchain

        Returns
        -------
        int
            block count
        """
        response = await self.__get_data(
            self.urls.get_block_count_url(coin_name=coin_name)
        )
        return int((response[self.urls.action_get_block_count][DATA]))

    async def async_get_block_stats(self, coin_name: str):
        """Get pool block stats

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        dict
            block stats
        """
        result = await self.__get_data(
            self.urls.get_block_stats_url(coin_name=coin_name)
        )
        return result[self.urls.action_get_block_stats][DATA]

    async def async_get_blocks_found(self, coin_name: str):
        """Get last N blocks found as configured in admin panel

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        list of dict:
            data for the last N blocks found
        """
        result = await self.__get_data(
            self.urls.get_blocks_found_url(coin_name=coin_name)
        )
        return result[self.urls.action_get_blocks_found][DATA]

    async def async_get_current_workers(self, coin_name: str):
        """Get the total hash rate of current workers for a coin pool

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        int
            the hash rate in kH/s
        """
        result = await self.__get_data(
            self.urls.get_current_workers_url(coin_name=coin_name)
        )
        return int(result[self.urls.action_get_current_workers][DATA])

    async def async_get_dashboard(self, coin_name: str):
        """Load a user's dashboard data for a pool: hash rate, share rate, balance, recent credits

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        dict
            dashboard data
        """
        result = await self.__get_data(
            self.urls.get_dashboard_data_url(coin_name=coin_name)
        )
        return result[self.urls.action_get_dashboard_data][DATA]

    async def async_get_difficulty(self, coin_name: str):
        """Get current difficulty in blockchain

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        int
            network difficulty
        """
        result = await self.__get_data(
            self.urls.get_difficulty_url(coin_name=coin_name)
        )
        return int(result[self.urls.action_get_difficulty][DATA])

    async def async_get_estimated_time(self, coin_name: str):
        """Get estimated time to next block based on pool hashrate (seconds)

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        int
            estimated time until next block in seconds
        """
        result = await self.__get_data(
            self.urls.get_estimated_time_url(coin_name=coin_name)
        )
        return int(result[self.urls.action_get_estimated_time][DATA])

    async def async_get_hourly_hash_rate(self, coin_name: str):
        """Get the average hash rate each hour for the last 24 hours, total and by worker, currently broken
        according to API docs

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        list of dict
            the first entry in the list is total hashrate, all following entries are for each worker
        """
        result = await self.__get_data(
            self.urls.get_hourly_hash_rates_url(coin_name=coin_name)
        )
        return result[self.urls.action_get_hourly_hash_rates][DATA]["mine"]

    async def async_get_nav_bar_data(self, coin_name: str):
        """Get the data displayed on the navbar. Always returns { "error": "disabled" }

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        dict of str
            error message
        """
        result = await self.__get_data(
            self.urls.get_nav_bar_data_url(coin_name=coin_name)
        )
        return result[self.urls.action_get_nav_bar_data][DATA]

    async def async_get_pool_hash_rate(self, coin_name: str):
        """Get current pool hash rate

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        float
            current pool hash rate in kH/s
        """
        result = await self.__get_data(
            self.urls.get_pool_hash_rate_url(coin_name=coin_name)
        )
        return result[self.urls.action_get_pool_hash_rate][DATA]

    async def async_get_pool_info(self, coin_name: str):
        """Get the information on pool settings

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        dict
            pool settings
        """
        result = await self.__get_data(self.urls.get_pool_info_url(coin_name=coin_name))
        return result[self.urls.action_get_pool_info][DATA]

    async def async_get_pool_share_rate(self, coin_name: str):
        """Get current pool share rate (shares/s)

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        int
            seems to always be 0
        """
        result = await self.__get_data(
            self.urls.get_pool_share_rate_url(coin_name=coin_name)
        )
        return result[self.urls.action_get_pool_share_rate]

    async def async_get_pool_status(self, coin_name: str):
        """Fetch overall pool status

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        dict
            pool status
        """
        result = await self.__get_data(
            self.urls.get_pool_status_url(coin_name=coin_name)
        )
        return result[self.urls.action_get_pool_status][DATA]

    async def async_get_time_since_last_block(self, coin_name: str):
        """Get time since last block found (seconds)

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        int
            time since last block found in seconds
        """
        result = await self.__get_data(
            self.urls.get_time_since_last_block_url(coin_name=coin_name)
        )
        return result[self.urls.action_get_time_since_last_block][DATA]

    async def async_get_top_contributors(self, coin_name: str):
        """Fetch top contributors data

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        dict
            returns account and hash rate as a dict
        """
        result = await self.__get_data(
            self.urls.get_top_contributors_url(coin_name=coin_name)
        )
        return result[self.urls.action_get_top_contributors][DATA]["hashes"]

    async def async_get_user_balance(self, coin_name: str):
        """Fetch a user's balance

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        dict of float
            returns confirmed and unconfirmed balances as a dict
        """
        result = await self.__get_data(
            self.urls.get_user_balance_url(coin_name=coin_name)
        )
        return result[self.urls.action_get_user_balance][DATA]

    async def async_get_user_hash_rate(self, coin_name: str):
        """Fetch a user's total hash rate

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        float
            total hash rate in kH/s
        """
        result = await self.__get_data(
            self.urls.get_user_hash_rate_url(coin_name=coin_name)
        )
        return result[self.urls.action_get_user_hash_rate][DATA]

    async def async_get_user_share_rate(self, coin_name: str):
        """Fetch a user's share rate

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        int
            seems to always be 0
        """
        result = await self.__get_data(
            self.urls.get_user_share_rate_url(coin_name=coin_name)
        )
        return result[self.urls.action_get_user_share_rate][DATA]

    async def async_get_user_status(self, coin_name: str):
        """Fetch a user's overall status

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        dict
            user status info: username, shares[valid|invalid|id|donate_percent|is_anonymous|username],
            hash rate, and share rate
        """
        result = await self.__get_data(
            self.urls.get_user_status_url(coin_name=coin_name)
        )
        return result[self.urls.action_get_user_status][DATA]

    async def async_get_user_transactions(self, coin_name: str):
        """Get a user's transactions

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        list of dict
            data on up to the last 30 transactions for a user on a pool
        """
        result = await self.__get_data(
            self.urls.get_user_transactions_url(coin_name=coin_name)
        )
        return result[self.urls.action_get_user_transactions][DATA]["transactions"]

    async def async_get_user_workers(self, coin_name: str):
        """Fetch a user's worker status

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        list of dict
            data on each worker represented as a dict: id, username, password, monitor, hash rate, difficulty
        """
        result = await self.__get_data(
            self.urls.get_user_workers_url(coin_name=coin_name)
        )
        return result[self.urls.action_get_user_workers][DATA]

    async def async_public(self, coin_name: str):
        """Fetch public pool statistics, no authentication required

        Parameters
        ----------
        coin_name : str
            coin to use for mining pool query

        Returns
        -------
        dict
            pool_name, hashrate, workers, shares_this_round, last_block, network_hashrate
        """
        return await self.__get_data(self.urls.public_url(coin_name))

    async def async_get_auto_switching_and_profits_statistics(self):
        """Get auto switching information for all algorithms

        Returns
        -------
        list of dict
            get list of auto switching statistics for each algorithm as a dict
        """
        path = self.urls.get_auto_switching_and_profits_statistics_url()
        response = await self.__get_data(path)
        if response["success"] is not True:
            raise APIError("Call failed")

        return response["return"]

    async def async_get_mining_profit_and_statistics(self):
        """Get mining profits statistics

        Returns
        -------
        list of dict
            mining statistics for each coin
        """
        path = self.urls.get_mining_profit_and_statistics_url()
        response = await self.__get_data(path)
        if response["success"] is not True:
            raise APIError("Call failed")

        return response["return"]

    async def async_get_user_all_balances(self):
        """Get all currency balances for a user

        Returns
        -------
        list of dict
            balances for each coin
        """
        result = await self.__get_data(self.urls.get_user_all_balances_url())
        return result[self.urls.action_get_user_all_balances][DATA]
