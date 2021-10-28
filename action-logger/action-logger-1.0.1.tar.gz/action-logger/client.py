# encoding: utf-8
import time
import inspect
import aiohttp
import asyncio
import requests
from functools import wraps

loop = asyncio.get_event_loop()


def get_client_info():
    """
    Get information from client.
    """
    import socket
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    data = {
        'hostname': hostname,
        'ip': ip
    }
    return data


async def push(session, url, data):
    async with session.post(url, json=data, timeout=0.2) as response:
        await response.text()


async def async_post(action_detail, action_timestamp):
    async with aiohttp.ClientSession() as session:
        data = get_client_info()
        data['action_detail'] = action_detail
        data['action_timestamp'] = action_timestamp
        await push(session, 'http://10.123.23.235:8001/save/test/post', data)


def post_client_info(action_detail, action_timestamp):
    """
    Sync
    Send client information
    """
    data = get_client_info()
    data['action_detail'] = action_detail
    data['action_timestamp'] = action_timestamp
    # 写成异步的形式
    res = requests.post('http://10.123.23.235:8001/save/test/post', json=data, timeout=(61, 61))
    print(res)
    print(res.json())


def action_post(function_to_protect):
    @wraps(function_to_protect)
    def wrapper(*args, **kwargs):
        action_detail = {
            'function_modele': function_to_protect.__module__,
            'function_name': function_to_protect.__name__,
            'function_doc': function_to_protect.__doc__,
            'function_parameters': [args, kwargs],
            'function_source_code': inspect.getsource(function_to_protect)
        }
        action_timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        # # sync
        # post_client_info(action_detail, action_timestamp)

        # async
        try:
            loop.run_until_complete(async_post(action_detail, action_timestamp))
        except Exception as e:
            print(f'Action logger: {e}')
        return function_to_protect(*args, **kwargs)

    return wrapper
