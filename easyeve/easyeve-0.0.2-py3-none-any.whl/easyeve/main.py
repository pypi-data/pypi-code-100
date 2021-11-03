#!/usr/bin/env python
import argparse
# import sys
import requests
import json
import os

def is_img(imgname):
    root, ext = os.path.splitext(imgname)
    if ext in ['.jpg', '.png', '.bmp', '.jpeg']:
        return True
    return False

def main():
    parser = argparse.ArgumentParser(description='Process some integers index.')

    # parser.add_argument('index', nargs='?', type=int, default=0,
    #                     help='an integer for download')

    parser.add_argument('list', nargs='?', type=int, default=0,
                        help='list the download list')

    parser.add_argument('--upload', 
                        help='upload file')

    args = parser.parse_args()

    if  args.upload is None and args.list is not None:
        p = args.list
        res = []
        id = ''
        for i in range(p+1):
            url = 'http://maiff.cn/maiff/api/tools/copy/copys' if i == 0 else 'http://maiff.cn/maiff/api/tools/copy/copys?id='+id
            r = requests.get(url)
            obj = json.loads(r.text)
            if i != 0:
                obj = list(reversed(obj))
            if len(obj) == 0:
                break
            id = obj[-1]['_id']['$oid']

            res+=obj
            
        for i,l in enumerate(res):
            print(i, '   ', l['content'])#, ' ', l['_id']['$oid'])

    # from pathlib import Path
    import os
    # import ipdb;ipdb.set_trace()
    if args.upload is not None:
        fname = args.upload
        if os.path.isfile(fname):
            if os.path.exists(fname):
                name = os.path.basename(fname)
                token = requests.get('http://maiff.cn/maiff/api/tools/qiniu/token?key='+name)
                token = json.loads(token.text)
                files = {'file': open(fname,'rb')}
                values = {'key': name, 'fname': name, 'token': token}
                print(values)
                d ={
                    "type": "file" if not is_img(fname) else "img",
                    "content": "//test.maiff.cn/"+name
                }
                r = requests.post('http://maiff.cn/maiff/api/tools/copy/copys', json=d)
                print(r.text)
                r = requests.post('https://upload.qiniup.com/', files=files, data=values)
                # r = requests.post('https://upload.qiniup.com/',  data=values)
                print(r.text)
            else:
                print('not exist')
        else:
            print('not file')

if __name__ == "__main__":
    main()
