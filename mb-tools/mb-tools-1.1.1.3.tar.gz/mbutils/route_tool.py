from importlib import import_module


def include(module):
    res = import_module(module)
    urls = getattr(res, 'urls')
    return urls


def url_wrapper(urls) -> list:
    wrapper_list = []
    for url in urls:
        path, handles = url
        if isinstance(handles, (tuple, list)):
            for handle in handles:
                pattern, handle_class = handle
                wrap = ('{0}{1}'.format(path, pattern), handle_class)
                wrapper_list.append(wrap)
        else:
            wrapper_list.append((path, handles))
    return wrapper_list


def create_handlers(router: str, ebike_router: str, callback) -> list:
    handlers = []
    # url映射
    handlers.extend(callback(router))
    handlers.extend(callback(f'{router}/v2'))

    if "share" in ebike_router:
        ROUTER_SHARE = f'/share{router}'
        ROUTER_SHARE_V2 = f'/share{router}/v2'
        handlers.extend(callback(ROUTER_SHARE))
        handlers.extend(callback(ROUTER_SHARE_V2))
    return handlers
