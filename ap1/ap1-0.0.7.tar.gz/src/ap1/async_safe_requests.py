import asyncio
import traceback
from .proxy import proxy_pack

METH_GET = "GET"
METH_POST = "POST"

class _SafeRequestContextManager:
    def __init__(self,session,proxy_dispatcher, logger, ATTEMPTS, ATTEMPT_DELAY, METHOD, url,**kwargs):
        self.session=session
        self.url=url
        self.proxy_dispatcher = proxy_dispatcher
        self.logger = logger
        self.ATTEMPTS = ATTEMPTS
        self.ATTEMPT_DELAY = ATTEMPT_DELAY
        self.METHOD = METHOD
        self.kwargs = kwargs

    async def __aenter__(self):
        attempt=0
        while True:
            proxy = self.proxy_dispatcher.syncGetProxy()
            try:
                self.logger.info(f"Async request:\nurl:{self.url}\tproxy:{proxy}")

                if self.METHOD == METH_GET:
                    self.res = await self.session.get(self.url, proxy=proxy, verify_ssl=False,**self.kwargs)
                elif self.METHOD == METH_POST:
                    self.res = await self.session.post(self.url, proxy=proxy, verify_ssl=False, **self.kwargs)
                else:
                    raise Exception(f"Incorrect request method: {self.METHOD}")

                return self.res
            except Exception as e:
                if not attempt < self.ATTEMPTS:
                    self.logger.error(e, traceback.format_exc())
                    return
                self.logger.warning(f"Attempt failed:\nurl:{self.url}\tproxy:{proxy}\nattempt:{attempt+1}\tmax attempts: {self.ATTEMPTS}")
                self.logger.warning(e,traceback.format_exc())
                attempt += 1
                await asyncio.sleep(self.ATTEMPT_DELAY)


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self,'res'):
            self.res.close()



class AsyncSafeRequests:
    def __init__(self,session, logger, ATTEMPTS, ATTEMPT_DELAY, proxy_channel, proxy_source):
        self.session = session
        self.logger=logger
        self.ATTEMPTS=ATTEMPTS
        self.ATTEMPT_DELAY=ATTEMPT_DELAY
        self.proxy_dispatcher = proxy_pack.ProxyDispatcher(proxy_channel, proxy_source)


    def get(self,url,**kwargs):
        return _SafeRequestContextManager(
            self.session,
            self.proxy_dispatcher,
            self.logger,
            self.ATTEMPTS,
            self.ATTEMPT_DELAY,
            METH_GET,
            url,
            **kwargs)

    def post(self,url,**kwargs):
        return _SafeRequestContextManager(
            self.session,
            self.proxy_dispatcher,
            self.logger,
            self.ATTEMPTS,
            self.ATTEMPT_DELAY,
            METH_POST,
            url,
            **kwargs)