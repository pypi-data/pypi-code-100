'''
    Bws Json RPC Client 
'''

from requests import post


class JsonRpcClient:
    def __init__(self, server="http://localhost:8181/jsonrpc", timeout=1, name=""):
        self.server = server
        self.timeout = timeout
        self._id = 0
        self.name = name

    @classmethod
    def call(cls, name, params={}, id=0, server="http://localhost:8181/jsonrpc", timeout=30):
        payload = {
            "method": name,
            "params": params,
            "jsonrpc": "2.0",
            "id": id,
        }
        return post(server, json=payload, timeout=timeout).json()

    def __call__(self, *args, **kwargs):
        if args:
            params = tuple(args)
            if len(kwargs):
                params += (kwargs,)
        else:
            params = kwargs
        self._id += 1
        return self.call(self.name, params, server=self.server, timeout=self.timeout, id=self._id)

    def get_function(self, name):
        def function(*args, **kwargs):
            # args_real = list(args) if args else kwargs
            if args:
                params = tuple(args)
                if len(kwargs):
                    params += (kwargs,)
            else:
                params = kwargs
            self._id += 1
            return self.call(name, params, server=self.server, timeout=self.timeout, id=self._id)

        return function

    def __getattr__(self, name):
        '''
            use:
                JsonRpcClient(2001).get_context()
        '''
        root = f"{self.name}." if self.name else ""
        return self.__class__(
            server=self.server,
            timeout=self.timeout,
            name=f"{root}{name}"
        )

    def __getitem__(self, name):
        '''
            use:
                JsonRpcClient(2001)["get_context"]()
        '''
        return self.get_function(name)


if __name__ == "__main__":
    api = JsonRpcClient("http://localhost:8181/rpc")
    r = api.sum(1, 2)
    print(r)
    r = api.sum(1, 2, type="B")
    print(r)
    r = api.apiview1.get_test(name="jad21", type="B")

    print(r)
