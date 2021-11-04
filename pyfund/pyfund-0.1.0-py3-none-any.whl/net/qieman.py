import requests

def get_date(code):


    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://qieman.com/funds/519915',
        'x-request-id': 'albus.FA2BF888D0E32D18BA4E',
        'x-sign': '1634696319438436022D7E3D4909C7A489A33A5146D00',
        'sensors-anonymous-id': '17c5eb933514c8-07ad687483a3f6-455f6c-2304000-17c5eb93352982',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'If-None-Match': 'W/"1ae8-a5pXu1QTBlgyp8MUcd8GhUTkLrs"',
    }

    response = requests.get('https://qieman.com/pmdj/v1/funds/{}'.format(code), headers=headers)
    print(">>>>>")
    print(response.status_code)
    print(response.text)
    print("??????")
