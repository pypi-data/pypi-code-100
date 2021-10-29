import time

import responses
import pytest
import httpretty
import requests
from requests.exceptions import HTTPError, RetryError, ReadTimeout
from vkinfo.exceptions import VkHttpError
from vkinfo.config import Default


@httpretty.activate
def test_max_retries(vk):
    httpretty.register_uri(
        httpretty.GET,
        "https://api.vk.com/method/example",
        responses=[
            httpretty.Response(
                body="",
                status=500,
            ),
            httpretty.Response(
                body="",
                status=500,
            ),
            httpretty.Response(
                body="",
                status=500,
            ),
        ],
    )
    with pytest.raises(SystemExit):
        _ = vk.method_execute(method="example")
    assert len(httpretty.latest_requests()) == 4

@httpretty.activate
def test_backoff_factor(vk):
    backoff_factor = Default.BACKOFF
    max_retries = Default.RETRIES
    total_delay = sum(backoff_factor * (2 ** n) for n in range(1, max_retries))

    httpretty.register_uri(
        httpretty.GET,
        "https://api.vk.com/method/example",
        responses=[
            httpretty.Response(
                body="",
                status=500,
            )
            for _ in range(max_retries)
        ],
    )
    start_time = time.time()
    with pytest.raises(SystemExit):
        # _ = vk.http.get("https://example.com/")
        vk.method_execute(method='example')
    end_time = time.time()
    time_diff = end_time - start_time

    assert time_diff == pytest.approx(total_delay, 0.1)
    assert max_retries + 1 ==  len(httpretty.latest_requests())

@responses.activate
def test_raises_client_error(vk, capsys):
    """test if exit code matches the one for timeout error"""

    responses.add(
        responses.GET,
        "https://api.vk.com/method/example",
        body=HTTPError())
    
    with pytest.raises(SystemExit) as errh:
        vk.method_execute(method='example')
    out, err = capsys.readouterr()
    assert errh.value.code == 4
    
@responses.activate
def test_raises_connection_error(vk, capsys):
    """test if exit code matches the one for timeout error"""

    responses.add(
        responses.GET,
        "https://api.vk.com/method/example",
        body=requests.ConnectionError())

    with pytest.raises(SystemExit) as errc:
        vk.method_execute(method='example')
    out, err = capsys.readouterr()
    print(out)
    assert errc.value.code == 5

@responses.activate
def test_raises_on_timeout_error(vk):
    """test if exit code matches the one for timeout error"""

    responses.add(
        responses.GET,
        "https://api.vk.com/method/example",
        body=ReadTimeout())

    with pytest.raises(SystemExit) as errt:
        vk.method_execute(method='example')
    assert errt.value.code == 6
    