import json
import sys
from . client import JsonRpcClient

def main():
    uri = sys.argv[1]
    method = sys.argv[2]
    params = sys.argv[3] if len(sys.argv) > 3 else '{}'

    api = JsonRpcClient(uri)
    print(sys.argv)
    try:
        r = api.call(method, json.loads(params), id=1, server=uri)
        r = r.get("result", r)
        r_json = json.dumps(r, indent=2)
        print(r_json)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
