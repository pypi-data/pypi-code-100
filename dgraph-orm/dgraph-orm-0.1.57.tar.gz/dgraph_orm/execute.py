import typing as T
import os
import time
import httpx
from httpx import Response
from . import GQLException

TIMEOUT = float(os.getenv("GQL_CLIENT_TIMEOUT", "25"))
print(f"{TIMEOUT=}")

client_sync = httpx.Client(timeout=TIMEOUT)
client = httpx.AsyncClient(timeout=TIMEOUT)


def check_for_errors(j: dict) -> None:
    if errors := j.get("errors"):
        raise GQLException(errors)


def finish(
    *, response: Response, query_str: str, should_print: bool, start_time: float
) -> dict:
    j = response.json()
    try:
        print(
            f"took: {(time.time() - start_time) * 1000}, "
            f'took internal: {int(j["extensions"]["tracing"]["duration"]) / (10 ** 6)}'
        )
    except Exception as e:
        print(f"ERRORED with {e=} IN FINISH, {j=}")
    if should_print:
        print(f"{query_str=}, {j=}")
    check_for_errors(j)
    if "data" not in j:
        raise GQLException(f"data not in j!, {j=}, {query_str=}")
    return j


async def gql(
    url: str,
    query_str: str,
    variables: dict = None,
    should_print: bool = False,
    use_one_time: bool = False,
) -> dict:
    start = time.time()
    json = {"query": query_str, "variables": variables or {}}
    if use_one_time:
        async with httpx.AsyncClient(timeout=TIMEOUT) as onetime_client:
            response = await onetime_client.post(url=url, json=json)
    else:
        response = await client.post(url=url, json=json)
    return finish(
        response=response,
        query_str=query_str,
        should_print=should_print,
        start_time=start,
    )
