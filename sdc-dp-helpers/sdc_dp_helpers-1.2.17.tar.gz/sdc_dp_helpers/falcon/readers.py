"""
    CUSTOM FALCON READER CLASSES
"""
import os
import time
from concurrent.futures import ThreadPoolExecutor

import requests

from sdc_dp_helpers.api_utilities.date_managers import date_handler, date_range
from sdc_dp_helpers.api_utilities.file_managers import load_file
from sdc_dp_helpers.api_utilities.retry_managers import request_handler, retry_handler


class CustomFalconReader:
    """
    Custom Falcon Reader
    """

    def __init__(self, creds_file, config_file=None):
        self._creds = load_file(creds_file, "yml")
        self._config = load_file(config_file, "yml")

        self.request_session = requests.Session()
        self.data_set = []

    @retry_handler(exceptions=ConnectionError, total_tries=5)
    def _get_channel_ids(self):
        """
        Gather all available channel ids.
        """
        print("GET: channels.")
        url = f"https://api.falcon.io/channels?apikey={self._creds['api_key']}"
        response = self.request_session.get(url=url, params={"limit": "999"})

        response_data = response.json()
        if response.status_code == 200:
            channel_ids = set()
            for item in response_data.get("items", []):
                channel_ids.add(item["id"])

            return channel_ids

        raise ConnectionError(
            f"Falcon API failed to return channel ids. "
            f"Status code: {response.status_code}."
        )

    @request_handler(
        wait=int(os.environ.get("REQUEST_WAIT_TIME", 5)),
        backoff_factor=float(os.environ.get("REQUEST_BACKOFF_FACTOR", 0.01)),
        backoff_method=os.environ.get("REQUEST_BACKOFF_METHOD", 0.01),
    )
    @retry_handler(exceptions=ConnectionError, total_tries=10, initial_wait=60)
    def _metrics_by_channel_handler(self, channel_id):
        """
        Request handler for Falcon metrics by channel.
        """
        print("GET: content metrics.")
        url = (
            f"https://api.falcon.io/measure/api/v1/content/metrics?"
            f"apikey={self._creds['api_key']}"
        )
        _date_fmt = "%Y-%m-%d"
        offset = 0
        while True:
            # for very large requests, split the query by day
            for date in date_range(
                start_date=date_handler(self._config.get("since", None), _date_fmt),
                end_date=date_handler(self._config.get("until", None), _date_fmt),
            ):
                print(f"Channel: {channel_id}. Offset: {offset}. Query date: {date}.")

                # set up payload that defines the response
                json_payload = {
                    "since": date,
                    "until": date,
                    "direction": self._config.get("direction", "ASC"),
                    "channels": [channel_id],
                    "metrics": self._config.get("metrics", []),
                    "offset": offset,
                }
                response = self.request_session.post(
                    url=url,
                    headers={"Content-Type": "application/json"},
                    json=json_payload,
                )

                if response.status_code == 200:
                    response_data = response.json()
                    if len(response_data) > 0:
                        offset += 1
                        print("Data returned.")
                        # response dataset from the offset
                        self.data_set.append(response_data[0])

                    else:
                        # simply print no data is returned to keep track of progress
                        print("No data returned.")
                        break

                elif response.status_code == 429:
                    print("Rolling Window Quota [429] reached, waiting for 15 minutes.")
                    time.sleep(900)

                elif response.status_code == 500:
                    raise ConnectionError(
                        "Status Code [500] returned."
                        "The reader configuration may be invalid."
                    )

                else:
                    # handle any unknown errors that are not pertinent to retrying
                    raise ConnectionError(
                        f"An unexpected error occurred [{response.status_code}] {response.reason}."
                    )

    def run_query(self):
        """
        Get metrics by channel Id context returns a request session with the ability
        to page with offsets.
        Content (or Post level) contains all metrics about your specific piece of
        content (posts). Here you will find impressions, reach, likes,
        shares and other metrics that show how well your specific post has performed.
        https://falconio.docs.apiary.io/reference/content-api/get-copied-content.
        """
        channel_ids = self._get_channel_ids()

        # process takes a couple of hours, so perhaps
        # running multiple channels at once will speed up the process
        max_threads = self._config.get("max_threads", None)
        if max_threads is not None:
            print(f"The reader will run max {max_threads} requests at once.")
            with ThreadPoolExecutor(max_workers=max_threads) as pool:
                # append all responses to the dataset
                pool.map(self._metrics_by_channel_handler, channel_ids)
        else:
            print("The reader will run 1 query at a time.")
            # optional basic query solution
            for channel_id in channel_ids:
                self._metrics_by_channel_handler(channel_id=channel_id)

        return self.data_set
