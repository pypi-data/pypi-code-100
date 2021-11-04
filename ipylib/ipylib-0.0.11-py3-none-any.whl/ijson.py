

import json
from io import StringIO


def read_req_headers(filepath):
    with open(file=filepath, mode='r') as f:
            text = f.read()
            f.close()

    headers = text.split('\n')
    js = {}
    for h in headers:
        # print(f"{h}\n\n")
        kv = h.split(':')
        if len(kv) is 2:
            js.update({kv[0].strip():kv[1].strip()})
    return js



def dump_json_into_file명(X_js, data_path, file명):
    """
    ensure_ascii=False --> 한글로 표시.
    """
    with open(data_path + file명, 'w') as f:
        json.dump(obj=X_js, fp=f, indent=4, ensure_ascii=False)
